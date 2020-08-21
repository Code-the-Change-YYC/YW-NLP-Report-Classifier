import axios from "axios";

export const getPrediction = async (description) => {
  const { data } = await axios.post("/api/predict/", { text: description });
  console.log(data);

  return data.sentiment;
};
