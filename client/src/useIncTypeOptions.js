import { useEffect, useState } from "react";
import { getMultiPrediction } from "./actions/predict";
import { useFormOptions } from "./useFormOptions";

export function useIncTypeOptions() {
  const { incTypes } = useFormOptions();

  const [incTypesOptions, setIncTypesOptions] = useState();
  const [incidentTypePri, setIncidentTypePri] = useState(null);

  async function updateOptionsFromDescription(description) {
    if (incTypesOptions) {
      const {updatedIncTypes, topIncType} = await getMultiPrediction(
        description,
        incTypesOptions
      );
      setIncTypesOptions(Object.values(updatedIncTypes));
      setIncidentTypePri(topIncType);
    }
  }

  // Fetch options only on component load
  useEffect(() => {
    if (incTypes) {
      setIncTypesOptions(incTypes)
    }
  }, [incTypes]);

  return {
    incidentTypePri,
    setIncidentTypePri,
    incTypesOptions,
    updateOptionsFromDescription,
  };
}
