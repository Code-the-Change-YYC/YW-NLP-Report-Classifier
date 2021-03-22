import axios from "axios";

export const getRedirectUrl = async (formData) => {
  const formFields = {
    ...formData,
    location: formData.location?.value,
    services_involved: (formData.services_involved || []).map((s) => s.value),
    incident_type_primary: formData.incident_type_primary?.value,
    incident_type_secondary: formData.incident_type_secondary?.value,
    child_involved: formData.child_involved?.value === "yes" ? true : false,
    non_client_involved:
      formData.non_client_involved?.value === "yes" ? true : false,
    program: formData.program?.value,
    immediate_response: formData.immediate_response.map((r) => r.value),
  };

  for (const [key, value] of Object.entries(formFields)) {
    if (value === "") {
      delete formFields[key];
    }
  }

  const { data } = await axios.post("/api/submit/", {
    form_fields: formFields,
  });

  if (data.redirect_url) {
    return data.redirect_url;
  }

  return "";
};
