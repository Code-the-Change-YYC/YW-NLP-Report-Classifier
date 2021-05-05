import { useState } from "react";

const useDateFieldInfo = (initiallyAutocomplete = true) => {
  const [userValue, setUserValue] = useState(null);
  const [autocompleteValue, setAutocompleteValue] = useState(null);
  const [useAutocomplete, setUseAutocompleteDefault] = useState(
    initiallyAutocomplete
  );
  const valid = useAutocomplete
    ? Boolean(autocompleteValue)
    : Boolean(userValue);
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

export default useDateFieldInfo;
