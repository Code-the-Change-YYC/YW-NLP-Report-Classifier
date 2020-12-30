import { useState } from "react";

const useTextFieldInfo = () => {
  const [info, setInfo] = useState({ user: "", autocomplete: "", useAutocomplete: true });
  const setUserValue = (value) => setInfo({ ...info, user: value });
  const setAutocompleteValue = (value) => setInfo({ ...info, autocomplete: value });
  const setUseAutocomplete = (useAutocomplete) => setInfo({ ...info, useAutocomplete });
  const valid = info.useAutocomplete ? info.autocomplete.length > 0 : info.user.length > 0;

  return [info, setUserValue, setAutocompleteValue, setUseAutocomplete, valid];
}

export default useTextFieldInfo;