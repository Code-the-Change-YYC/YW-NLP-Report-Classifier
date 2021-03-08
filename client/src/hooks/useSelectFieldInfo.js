import { useState } from "react";

const useSelectFieldInfo = () => {
  const [userValue, setUserValue] = useState(null);
  const [autocompleteValue, setAutocompleteValue] = useState(null);
  const [useAutocomplete, setUseAutocompleteDefault] = useState(true);
  const valid = useAutocomplete
    ? autocompleteValue !== undefined
    : userValue !== undefined;
  const value = useAutocomplete ? autocompleteValue : userValue;

  function setUseAutocomplete(newValue) {
    // if no argument, toggle
    if (newValue === undefined) {
      setUseAutocompleteDefault(!useAutocomplete);
      return;
    }

    setUseAutocompleteDefault(newValue);
  }

  return [
    value,
    setUserValue,
    setAutocompleteValue,
    useAutocomplete,
    setUseAutocomplete,
    valid,
  ];
};

export default useSelectFieldInfo;
