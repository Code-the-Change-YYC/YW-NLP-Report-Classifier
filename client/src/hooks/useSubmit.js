import { useState } from "react";
import { getRedirectUrl } from "../actions/submit";

const useSubmit = ({
  description,
  clientInitials,
  clientSecInitials,
  location,
  locationDetail,
  servicesInvolved,
  otherServices,
  staffInvolvedFirst,
  staffInvolvedLast,
  dateOccurred,
  incidentTypePri,
  incidentTypeSec,
  involvesChild,
  involvesNonClient,
  program,
  immediateResponse,
  staffCompleting,
  supervisorReviewer,
  dateCompleted,
  clientInitialsValid,
  locationValid,
  dateOccurredValid,
  involvesChildValid,
  programValid,
  incidentTypePriValid,
}) => {
  const [submitClicked, setSubmitClicked] = useState(false);

  const submitWarningStyle = (val) => {
    if (
      submitClicked &&
      (val === null || val === undefined || val.length === 0)
    ) {
      return { border: "1px solid red" };
    }
    return {};
  };

  const checkRequiredFields = () => {
    return (
      description &&
      clientInitialsValid &&
      locationValid &&
      dateOccurredValid &&
      incidentTypePriValid &&
      involvesChildValid &&
      programValid &&
      immediateResponse &&
      staffCompleting &&
      supervisorReviewer
    );
  };

  const handleSubmit = async function (e) {
    e.preventDefault();
    // window.open(
    //   "https://docs.google.com/forms/d/e/1FAIpQLScfxUsVQDwfXkUeVqfHQrhJpUv9_COL6_9bxgXEAL3M_NA5og/viewform?usp=sf_link"
    // );
    const formData = {
      description,
      client_primary: clientInitials,
      client_secondary: clientSecInitials,
      location,
      location_detail: locationDetail,
      services_involved: servicesInvolved,
      services_involved_other: otherServices,
      primary_staff_first_name: staffInvolvedFirst,
      primary_staff_last_name: staffInvolvedLast,
      occurrence_time: dateOccurred,
      incident_type_primary: incidentTypePri,
      incident_type_secondary: incidentTypeSec,
      child_involved: involvesChild,
      non_client_involved: involvesNonClient,
      program,
      immediate_response: immediateResponse,
      staff_name: staffCompleting,
      program_supervisor_reviewer_name: supervisorReviewer,
      completion_date: dateCompleted,
    };
    const redirectUrl = await getRedirectUrl(formData);
    console.log(redirectUrl);
    window.location.href = redirectUrl;
  };

  return {
    submitClicked,
    setSubmitClicked,
    submitWarningStyle,
    handleSubmit,
    checkRequiredFields,
  };
};

export default useSubmit;
