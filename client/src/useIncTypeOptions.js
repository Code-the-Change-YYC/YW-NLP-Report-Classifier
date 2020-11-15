import { useEffect, useState } from "react";
import { getMultiPrediction } from "./actions/predict";
import { useFormOptions } from "./useFormOptions";

function incTypesToReactSelectOptions(incTypes) {
  return Object.assign(
    {},
    ...incTypes.map((incType) => {
      const value = incType.toLowerCase();
      return {
        [value]: {
          value,
          label: incType,
        },
      };
    })
  );
}

export function useIncTypeOptions() {
  const { incTypes } = useFormOptions();

  const [incTypesOptions, setIncTypesOptions] = useState();
  const [incidentTypePri, setIncidentTypePri] = useState(null);

  async function updateOptionsFromDescription(description) {
    if (incTypesOptions) {
      const predictions = await getMultiPrediction(
        description,
        incTypesOptions
      );
      setIncTypesOptions(predictions);
      setIncidentTypePri(predictions[0]);
    }
  }

  // Fetch options only on component load
  useEffect(() => {
    if (incTypes) {
      setIncTypesOptions(incTypesToReactSelectOptions(incTypes));
    }
  }, [incTypes]);

  const reactSelectOptions = incTypesOptions
    ? Object.values(incTypesOptions)
    : null;

  return {
    incidentTypePri,
    setIncidentTypePri,
    reactSelectOptions,
    updateOptionsFromDescription,
  };
}
