import axios from 'axios'

export const getPrediction = async (description) => {
    const { data } = await axios.post('/api/predict/', { text: description })
    console.log(data)

    return data.prediction.toLowerCase()
}

export const getMultiPrediction = async (description) => {
    const { data } = await axios.post('/api/predict_multiple/', {
        text: description,
        num_predictions: 5,
    })
    return data.predictions.map((pred) => [pred[0].toLowerCase(), pred[1]])
}
