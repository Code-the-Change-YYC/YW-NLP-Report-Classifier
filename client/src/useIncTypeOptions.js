import { useEffect, useState } from "react";
import { getMultiPrediction } from "./actions/predict";
import { useFormOptions } from "./useFormOptions";
import useSelectFieldInfo from "./hooks/useSelectFieldInfo";

export function useIncTypeOptions() {
  const [
    incidentTypePri,
    setIncidentTypePri,
    setIncidentTypePriAutocomplete,
    setIncidentTypePriShowAutocomplete,
    incidentTypePriValid,
  ] = useSelectFieldInfo();

  const { incTypes } = useFormOptions();

  const [incTypesOptions, setIncTypesOptions] = useState();

  async function updateOptionsFromDescription(description) {
    if (incTypesOptions) {
      const { updatedIncTypes, topIncType } = await getMultiPrediction(
        description,
        incTypesOptions
      );
      setIncTypesOptions(Object.values(updatedIncTypes));
      setIncidentTypePriAutocomplete(topIncType);
    }
  }

  // Fetch options only on component load
  useEffect(() => {
    if (incTypes) {
      setIncTypesOptions(incTypes);
    }
  }, [incTypes]);

  return {
    incidentTypePri,
    setIncidentTypePri,
    setIncidentTypePriAutocomplete,
    setIncidentTypePriShowAutocomplete,
    incidentTypePriValid,
    incTypesOptions,
    updateOptionsFromDescription,
  };
}
