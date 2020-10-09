import axios from "axios";
import { incidentTypes } from "../formOptions";

export const getMultiPrediction = async (description) => {
  const { data } = await axios.post("/api/predict/", {
    text: description,
    num_predictions: 21,
  });
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
