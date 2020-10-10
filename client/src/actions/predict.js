import axios from 'axios'

export const getMultiPrediction = async (description, incidentTypes) => {
    const { data } = await axios.post('/api/predict/', {
        text: description,
        num_predictions: 21,
    })
    if (data.predictions) {
        return Object.assign(
            incidentTypes,
            ...data.predictions.map((pred) => {
                const [incType, confidenceVal] = pred
                const reactSelectOption = incidentTypes[incType.toLowerCase()]
                const value = reactSelectOption.value
                return {
                    [value]: {
                        label: reactSelectOption.label,
                        value,
                        confidenceVal: (confidenceVal * 10).toFixed(2),
                    },
                }
            })
        )
    }
    return []
}
