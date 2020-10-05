import axios from "axios";
import { incidentTypes } from "../formOptions";

export const getPrediction = async (description) => {
  const { data } = await axios.post("/api/predict/", { text: description });
  console.log(data);

  return data.prediction.toLowerCase();
};

export const getMultiPrediction = async (description) => {
  const { data } = await axios.post("/api/predict_multiple/", {
    text: description,
    num_predictions: 21,
  });
  console.log({ data });
  if (data.predictions) {
    return data.predictions.map((pred) => {
      const [incType, confidenceVal] = pred;
      const reactSelectOption = incidentTypes[incType.toLowerCase()];
      return {
        label: reactSelectOption.label,
        value: reactSelectOption.value,
        confidenceVal: (confidenceVal * 10).toFixed(2),
      };
    });
  }
  return [];
};
