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

  const checkCovidSpecialCase = (desc, keywords) => {
    const lowercasedDescription = desc.toLowerCase();
    return (
      keywords.find((keyword) =>
        lowercasedDescription.includes(keyword.toLowerCase())
      ) || null
    );
  };

  const updateOptionsFromDescription = useCallback(
    async (description, options) => {
      // specialcase to be handled for Covid keywords
      const covidKeywords = ["covid", "coronavirus"];

      if (options) {
        const covidOptionIfExists = options.find((type) =>
          type.label.toLowerCase().includes("covid-19 confirmed")
        );

        if (
          checkCovidSpecialCase(description, covidKeywords) != null &&
          covidOptionIfExists
        ) {
          setIncTypesOptions(Object.values(options));
          setIncidentTypePriAutocomplete({
            ...covidOptionIfExists,
            confidence: 1.0,
          });
        } else {
          const { updatedIncTypes, topIncType } = await getMultiPrediction(
            description,
            options
          );

          setIncTypesOptions(Object.values(updatedIncTypes));
          setIncidentTypePriAutocomplete(topIncType);
        }
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
