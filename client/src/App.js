import React, { useState } from "react";
import styled from "styled-components";
import logo from "./logo.jpg";
import "./App.css";
import { FormRow, Input, Textarea, HR } from "./styled";

import TextInput from "./components/TextInput";
import Select from "react-select";
import SelectInput from "./components/SelectInput";
import DateInput from "./components/DateInput";
import ReactDatePicker from "react-datepicker";
import IncTypePrimaryField from "./components/IncTypePrimaryField";
import ModalBox from "./components/ModalBox";
import FeedbackBox from "./components/FeedbackBox";

import useTextFieldInfo from "./hooks/useTextFieldInfo";
import useSelectFieldInfo from "./hooks/useSelectFieldInfo";
import useDateFieldInfo from "./hooks/useDateFieldInfo";
import { useFormOptions } from "./hooks/useFormOptions";
import { useIncTypeOptions } from "./hooks/useIncTypeOptions";
import useAutocomplete from "./hooks/useAutocomplete";
import useSubmit from "./hooks/useSubmit";

const LastUpdated = styled.h2`
  font-size: 12pt;
`;

function App() {
  // State variables
  const [description, setDescription] = useState("");

  const [
    clientInitials,
    setClientInitials,
    setClientInitialsAutocomplete,
    clientInitialsShowAutocomplete,
    setClientInitialsShowAutocomplete,
    clientInitialsValid,
  ] = useTextFieldInfo();
  const [
    clientSecInitials,
    setClientSecInitials,
    setClientSecInitialsAutocomplete,
    clientSecInitialsShowAutocomplete,
    setClientSecInitialsShowAutocomplete,
  ] = useTextFieldInfo();
  const [
    location,
    setLocation,
    setLocationAutocomplete,
    locationShowAutocomplete,
    setLocationShowAutocomplete,
    locationValid,
  ] = useSelectFieldInfo();

  const [locationDetail, setLocationDetail] = useState("");

  const [
    servicesInvolved,
    setServicesInvolved,
    setServicesInvolvedAutocomplete,
    servicesInvolvedShowAutocomplete,
    setServicesInvolvedShowAutocomplete,
  ] = useSelectFieldInfo();

  const [otherServices, setOtherServices] = useState("");
  const [staffInvolvedFirst, setStaffInvolvedFirst] = useState("");
  const [staffInvolvedLast, setStaffInvolvedLast] = useState("");
  const [
    dateOccurred,
    setDateOccurred,
    setDateOccurredAutocomplete,
    dateOccurredShowAutocomplete,
    setDateOccurredShowAutocomplete,
    dateOccurredValid,
  ] = useDateFieldInfo(false);

  const [incidentTypeSec, setIncidentTypeSec] = useState(null);
  const [otherSecIncidentType, setOtherSecIncidentType] = useState("");

  const [
    involvesChild,
    setInvolvesChild,
    setInvolvesChildAutocomplete,
    involvesChildShowAutocomplete,
    setInvolvesChildShowAutocomplete,
    involvesChildValid,
  ] = useSelectFieldInfo();

  const [
    involvesNonClient,
    setInvolvesNonClient,
    setInvolvesNonClientAutocomplete,
    involvesNonClientShowAutocomplete,
    setInvolvesNonClientShowAutocomplete,
  ] = useSelectFieldInfo();

  const [
    program,
    setProgram,
    setProgramAutocomplete,
    programShowAutocomplete,
    setProgramShowAutocomplete,
    programValid,
  ] = useSelectFieldInfo();

  const [
    immediateResponse,
    setImmediateResponse,
    setImmediateResponseAutocomplete,
    immediateResponseShowAutocomplete,
    setImmediateResponseShowAutocomplete,
  ] = useSelectFieldInfo();

  const [staffCompleting, setStaffCompleting] = useState("");
  const [supervisorReviewer, setSupervisorReviewer] = useState("");
  const [dateCompleted, setDateCompleted] = useState(new Date());
  const [modalDisplay, setModalDisplay] = useState("none");

  const {
    incidentTypePri,
    setIncidentTypePri,
    incidentTypePriShowAutocomplete,
    setIncidentTypePriShowAutocomplete,
    incTypesOptions,
    sortedIncTypeOptions,
    updateOptionsFromDescription: updateIncTypesOptions,
    incidentTypePriValid,
  } = useIncTypeOptions();

  const {
    locations,
    programs,
    immediateResponses,
    services,
    childInvolvedOptions,
    guestInvolvedOptions,
  } = useFormOptions();

  const formData = {
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
  };

  useAutocomplete({
    description,
    immediateResponses,
    immediateResponse,
    services,
    locations,
    programs,
    clientInitials,
    incTypesOptions,
    childInvolvedOptions,
    guestInvolvedOptions,
    setImmediateResponseAutocomplete,
    setServicesInvolvedAutocomplete,
    setLocationAutocomplete,
    setProgramAutocomplete,
    setDateOccurredAutocomplete,
    setClientInitialsAutocomplete,
    setClientSecInitialsAutocomplete,
    updateIncTypesOptions,
    setInvolvesChildAutocomplete,
    setInvolvesNonClientAutocomplete,
  });

  const {
    submitClicked,
    setSubmitClicked,
    submitWarningStyle,
    handleSubmit,
    checkRequiredFields,
  } = useSubmit(formData);

  return (
    <div className="App">
      <ModalBox
        formData={formData}
        modalDisplay={modalDisplay}
        setModalDisplay={setModalDisplay}
        handleSubmit={handleSubmit}
      ></ModalBox>
      <img src={logo} alt="YW logo"></img>
      <h1>Critical Incident Report Form</h1>
      <LastUpdated>Last updated: June 2, 2021</LastUpdated>
      <FormRow>
        <label>Description of Incident *</label>
        <Textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={7}
          style={{ ...submitWarningStyle(description) }}
          spellCheck
        ></Textarea>
      </FormRow>
      <HR></HR>
      <form>
        <FormRow style={{ flexDirection: "row" }}>
          <TextInput
            label="Client Involved - Primary (Initials)"
            required
            value={clientInitials}
            setValue={setClientInitials}
            showAutocomplete={clientInitialsShowAutocomplete}
            setShowAutocomplete={setClientInitialsShowAutocomplete}
            submitClicked={submitClicked}
            customStyle={{ width: "95%" }}
          ></TextInput>
          <TextInput
            label="Client Involved - Secondary (Initials)"
            value={clientSecInitials}
            setValue={setClientSecInitials}
            showAutocomplete={clientSecInitialsShowAutocomplete}
            setShowAutocomplete={setClientSecInitialsShowAutocomplete}
            submitClicked={submitClicked}
          ></TextInput>
        </FormRow>

        <FormRow style={{ flexDirection: "row" }}>
          <SelectInput
            label="Location"
            options={locations}
            value={location}
            setValue={setLocation}
            showAutocomplete={locationShowAutocomplete}
            setShowAutocomplete={setLocationShowAutocomplete}
            submitClicked={submitClicked}
            required
            customStyle={{ width: "95%" }}
          ></SelectInput>

          <div style={{ width: "100%" }}>
            <label>Location Detail</label>
            <Input
              value={locationDetail}
              onChange={(e) => setLocationDetail(e.target.value)}
            ></Input>
          </div>
        </FormRow>

        <FormRow style={{ flexDirection: "row" }}>
          <SelectInput
            label="Services Involved"
            options={services}
            value={servicesInvolved}
            setValue={setServicesInvolved}
            showAutocomplete={servicesInvolvedShowAutocomplete}
            setShowAutocomplete={setServicesInvolvedShowAutocomplete}
            submitClicked={submitClicked}
            isMulti
            customStyle={{ width: "95%" }}
          ></SelectInput>

          <div style={{ width: "100%" }}>
            <label
              style={
                (servicesInvolved || []).some((s) => s.value === "other")
                  ? { fontWeight: "bold" }
                  : {}
              }
            >
              Other Services Involved (if other)
            </label>
            <Input
              value={otherServices}
              onChange={(e) => setOtherServices(e.target.value)}
            ></Input>
          </div>
        </FormRow>

        <FormRow style={{ flexDirection: "row" }}>
          <div style={{ width: "100%" }}>
            <label>Primary Staff Involved First Name</label>
            <Input
              value={staffInvolvedFirst}
              onChange={(e) => setStaffInvolvedFirst(e.target.value)}
              style={{ width: "95%" }}
            ></Input>
          </div>
          <div style={{ width: "100%" }}>
            <label>Primary Staff Involved Last Name</label>
            <Input
              value={staffInvolvedLast}
              onChange={(e) => setStaffInvolvedLast(e.target.value)}
            ></Input>
          </div>
        </FormRow>

        <FormRow>
          <DateInput
            label="Date and Time of Occurrence"
            value={dateOccurred}
            setValue={setDateOccurred}
            showAutocomplete={dateOccurredShowAutocomplete}
            setShowAutocomplete={setDateOccurredShowAutocomplete}
            required
            submitClicked={submitClicked}
          ></DateInput>
        </FormRow>

        <FormRow style={{ flexDirection: "row" }}>
          <IncTypePrimaryField
            incidentType={incidentTypePri}
            setIncidentType={setIncidentTypePri}
            sortedIncTypeOptions={sortedIncTypeOptions}
            showAutocomplete={incidentTypePriShowAutocomplete}
            setShowAutocomplete={setIncidentTypePriShowAutocomplete}
            submitClicked={submitClicked}
          ></IncTypePrimaryField>

          <div style={{ width: "100%" }}>
            <label>Incident Type (Secondary)</label>
            <Select
              value={incidentTypeSec}
              onChange={(incidentType) => {
                setIncidentTypeSec(incidentType);
              }}
              options={sortedIncTypeOptions}
            ></Select>
          </div>
        </FormRow>
        <FormRow
          style={{
            display:
              incidentTypeSec && incidentTypeSec.value === "other"
                ? "flex"
                : "none",
            flexDirection: "row",
          }}
        >
          <div style={{ width: "100%" }}></div>
          <div style={{ width: "100%" }}>
            <label>Secondary Incident Type</label>
            <Input
              value={otherSecIncidentType}
              onChange={(e) => setOtherSecIncidentType(e.target.value)}
            ></Input>
          </div>
        </FormRow>
        <FormRow style={{ flexDirection: "row" }}>
          <SelectInput
            label="Did this incident involve a child?"
            required
            options={childInvolvedOptions}
            value={involvesChild}
            setValue={setInvolvesChild}
            showAutocomplete={involvesChildShowAutocomplete}
            setShowAutocomplete={setInvolvesChildShowAutocomplete}
            submitClicked={submitClicked}
            customStyle={{ width: "95%" }}
          ></SelectInput>

          <SelectInput
            label="Did this incident involve a non-client guest?"
            options={guestInvolvedOptions}
            value={involvesNonClient}
            setValue={setInvolvesNonClient}
            showAutocomplete={involvesNonClientShowAutocomplete}
            setShowAutocomplete={setInvolvesNonClientShowAutocomplete}
            submitClicked={submitClicked}
            customStyle={{ width: "100%" }}
          ></SelectInput>
        </FormRow>

        <FormRow>
          <SelectInput
            label="Program"
            options={programs}
            value={program}
            setValue={setProgram}
            showAutocomplete={programShowAutocomplete}
            setShowAutocomplete={setProgramShowAutocomplete}
            submitClicked={submitClicked}
            required
          ></SelectInput>
        </FormRow>
        <FormRow>
          <SelectInput
            label="Immediate Response to the Incident"
            options={immediateResponses}
            value={immediateResponse}
            setValue={setImmediateResponse}
            showAutocomplete={immediateResponseShowAutocomplete}
            setShowAutocomplete={setImmediateResponseShowAutocomplete}
            submitClicked={submitClicked}
            required
            isMulti
          ></SelectInput>
        </FormRow>
        <FormRow style={{ flexDirection: "row" }}>
          <div style={{ width: "100%" }}>
            <label>Name of Staff Completing this Report *</label>
            <Input
              value={staffCompleting}
              onChange={(e) => setStaffCompleting(e.target.value)}
              style={{ width: "95%", ...submitWarningStyle(staffCompleting) }}
            ></Input>
          </div>
          <div style={{ width: "100%" }}>
            <label>Name of Program Supervisor Reviewer *</label>
            <Input
              value={supervisorReviewer}
              onChange={(e) => setSupervisorReviewer(e.target.value)}
              style={{ ...submitWarningStyle(supervisorReviewer) }}
            ></Input>
          </div>
        </FormRow>
        <FormRow>
          <label>Completed On *</label>
          <ReactDatePicker
            value={Date.now()}
            selected={dateCompleted}
            setDate={setDateCompleted}
            onChange={(date) => {
              setDateCompleted(date);
            }}
            customInput={<Input></Input>}
            showTimeSelect
            timeIntervals={15}
            dateFormat="MMMM d, yyyy h:mm aa"
          ></ReactDatePicker>
        </FormRow>
        <input
          type="submit"
          value="Next"
          onClick={(e) => {
            e.preventDefault();
            setSubmitClicked(true);
            if (checkRequiredFields()) {
              setModalDisplay("block");
            }
          }}
        ></input>
      </form>
      <FeedbackBox />
    </div>
  );
}

export default App;
