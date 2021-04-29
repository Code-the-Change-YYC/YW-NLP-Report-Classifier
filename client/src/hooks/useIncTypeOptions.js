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

  const covidKeywords = ["covid19","covid","coronavirus"];

  const covidException = (desc, keywords) => {
    const lowercasedDescription = desc.toLowerCase();
    return (
      keywords.find((keyword) =>
          lowercasedDescription.includes(keyword.toLowerCase()
          )
      ) || null
    );
  };

  const updateOptionsFromDescription = useCallback(
    async (description, options) => {
       // specialcase to be handled for Covid keywords

      if (options) {
        if(covidException(description,covidKeywords)!= null){
        
          setIncTypesOptions(Object.values(options));
          setIncidentTypePriAutocomplete({label: "COVID-19 Confirmed", 
                                          value: "COVID-19 Confirmed", 
                                          confidence: "1"});
         
          }
        else{
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
