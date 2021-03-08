import { useEffect, useState, useCallback } from "react";
import { getMultiPrediction } from "../actions/predict";
import { useFormOptions } from "./useFormOptions";
import useSelectFieldInfo from "./useSelectFieldInfo";

export function useIncTypeOptions() {
  const [
    incidentTypePri,
    setIncidentTypePri,
    setIncidentTypePriAutocomplete,
    incidentTypePriShowAutocomplete,
    setIncidentTypePriShowAutocomplete,
    incidentTypePriValid,
  ] = useSelectFieldInfo();

  const { incTypes } = useFormOptions();

  const [incTypesOptions, setIncTypesOptions] = useState();

  const updateOptionsFromDescription = useCallback(
    async (description, options) => {
      if (options) {
        const { updatedIncTypes, topIncType } = await getMultiPrediction(
          description,
          options
        );
        setIncTypesOptions(Object.values(updatedIncTypes));
        setIncidentTypePriAutocomplete(topIncType);
      }
    },
    [setIncTypesOptions, setIncidentTypePriAutocomplete]
  );

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
    incidentTypePriShowAutocomplete,
    setIncidentTypePriShowAutocomplete,
    incidentTypePriValid,
    incTypesOptions,
    sortedIncTypeOptions,
    updateOptionsFromDescription,
  };
}
