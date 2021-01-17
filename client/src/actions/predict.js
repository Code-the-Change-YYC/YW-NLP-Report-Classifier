import axios from 'axios'


/**
 * Use sigmoid function to put confidence values on a scale of 0 to 1.
 * 
 * @param {Array} confidenceValues 
 */
function getConfidenceDisplayValues(confidenceValues) {
  // Update this to increase/decrease the difference between the outputed
  // confidence values
  const scaleFactor = 10;
  return confidenceValues.map((v) => 1 / (1 + Math.exp(-v * scaleFactor)));
}


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
        const confValues = getConfidenceDisplayValues(
          data.predictions.map(([_, c]) => c)
        );
        const updatedIncTypes = Object.assign(
            incidentTypesLookup,
            ...data.predictions.map(([incType], i) => {
                const confidence = confValues[i];
                const reactSelectOption =
                    incidentTypesLookup[incType.toLowerCase()]
                const value = reactSelectOption.value
                return {
                    [value]: {
                        label: reactSelectOption.label,
                        value,
                        confidence: confidence.toFixed(2),
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
