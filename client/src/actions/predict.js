import axios from "axios";
import { incidentTypes } from "../formOptions";

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

export const getMultiPrediction = async (description) => {
  const { data } = await axios.post("/api/predict/", {
    text: description,
    num_predictions: 21,
  });
  if (data.predictions) {
    const confValues = getConfidenceDisplayValues(
      data.predictions.map(([_, c]) => c)
    );
    return data.predictions.map(([incType], i) => {
      const confidence = confValues[i];
      const reactSelectOption = incidentTypes.find(
        (i) => i.label.toLowerCase() === incType.toLowerCase()
      );
      return {
        label: reactSelectOption.label,
        value: reactSelectOption.value,
        confidence: confidence.toFixed(2),
      };
    });
  }
  return [];
};
