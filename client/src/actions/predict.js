import axios from 'axios'

/**
 * Creates an object mapping incident type option `value` keys to their object.
 * 
 * @param {array} incTypesOptions React select options
 */
function getIncTypesLookup(incTypesOptions) {
    return Object.assign(
        {},
        ...incTypesOptions.map((incTypeOption) => {
            return {
                [incTypeOption.value]: incTypeOption,
            }
        })
    )
}

/**
 * Gets incident type predictions for the given description.
 * 
 * @param {string} description To predict incident type of
 * @param {array} incidentTypes React select options
 */
export const getMultiPrediction = async (description, incidentTypes) => {
    const { data } = await axios.post('/api/predict/', {
        text: description,
        num_predictions: incidentTypes.length,
    })
    if (data.predictions) {
        const incidentTypesLookup = getIncTypesLookup(incidentTypes)
        const updatedIncTypes = Object.assign(
            incidentTypesLookup,
            ...data.predictions.map((pred) => {
                const [incType, confidenceVal] = pred
                const reactSelectOption =
                    incidentTypesLookup[incType.toLowerCase()]
                const value = reactSelectOption.value
                return {
                    [value]: {
                        label: reactSelectOption.label,
                        value,
                        confidence: (confidenceVal * 10).toFixed(2),
                    },
                }
            })
        )
        return {
            updatedIncTypes,
            topIncType: updatedIncTypes[data.predictions[0][0].toLowerCase()],
        }
    }
    return {}
}
