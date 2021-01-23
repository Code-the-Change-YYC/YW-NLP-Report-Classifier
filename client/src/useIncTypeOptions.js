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

  const sortedIncTypeOptions = incTypesOptions?.sort((firstEl, secondEl) => {
    if (firstEl.confidence && secondEl.confidence) {
      return (
        Number.parseFloat(secondEl.confidence) -
        Number.parseFloat(firstEl.confidence)
      );
    }
  });
  return {
    incidentTypePri,
    setIncidentTypePri,
    setIncidentTypePriAutocomplete,
    setIncidentTypePriShowAutocomplete,
    incidentTypePriValid,
    sortedIncTypeOptions,
    updateOptionsFromDescription,
  };
}
