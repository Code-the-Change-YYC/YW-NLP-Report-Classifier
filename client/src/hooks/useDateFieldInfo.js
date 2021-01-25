import { useState } from "react";

const useDateFieldInfo = () => {
  const [userValue, setUserValue] = useState(new Date());
  const [autocompleteValue, setAutocompleteValue] = useState(new Date());
  const [useAutocomplete, setUseAutocompleteDefault] = useState(true);
  const valid = useAutocomplete ? autocompleteValue : userValue;
  const value = useAutocomplete ? autocompleteValue : userValue;

  function setUseAutocomplete(newValue) {
    // if no argument, toggle
    if (newValue === undefined) {
      setUseAutocompleteDefault(!useAutocomplete);
      return;
    }

    setUseAutocompleteDefault(newValue);
  }

  return [value, setUserValue, setAutocompleteValue, setUseAutocomplete, valid];
};

export default useDateFieldInfo;
