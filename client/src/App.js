import { useFormOptions } from "./hooks/useFormOptions";
import { useIncTypeOptions } from "./hooks/useIncTypeOptions";
import React, { useState } from "react";
import logo from "./logo.jpg";
import "./App.css";
import Select from "react-select";
import { FormRow, Input, Textarea, HR, ModalClose } from "./styled";
import TextInput from "./components/TextInput";
import useTextFieldInfo from "./hooks/useTextFieldInfo";
import useSelectFieldInfo from "./hooks/useSelectFieldInfo";
import useDateFieldInfo from "./hooks/useDateFieldInfo";
import useSubmit from "./hooks/useSubmit";
import SelectInput from "./components/SelectInput";
import DateInput from "./components/DateInput";
import FeedbackBox from "./components/FeedbackBox";
import IncTypePrimaryField from "./components/IncTypePrimaryField";
import ReactDatePicker from "react-datepicker";
import useAutocomplete from "./hooks/useAutocomplete";

function App() {
  // State variables
  const [description, setDescription] = useState("");

  const [
    clientInitials,
    setClientInitials,
    setClientInitialsAutocomplete,
    setClientInitialsShowAutocomplete,
    clientInitialsValid,
  ] = useTextFieldInfo();
  const [
    clientSecInitials,
    setClientSecInitials,
    setClientSecInitialsAutocomplete,
    setClientSecInitialsShowAutocomplete,
  ] = useTextFieldInfo();
  const [
    location,
    setLocation,
    setLocationAutocomplete,
    setLocationShowAutocomplete,
  ] = useSelectFieldInfo();

  const [locationDetail, setLocationDetail] = useState("");

  const [
    servicesInvolved,
    setServicesInvolved,
    setServicesInvolvedAutocomplete,
    setServicesInvolvedShowAutocomplete,
  ] = useSelectFieldInfo();

  const [otherServices, setOtherServices] = useState("");
  const [staffInvolvedFirst, setStaffInvolvedFirst] = useState("");
  const [staffInvolvedLast, setStaffInvolvedLast] = useState("");
  const [
    dateOccurred,
    setDateOccurred,
    setDateOccurredAutocomplete,
    setDateOccurredShowAutocomplete,
  ] = useDateFieldInfo();

  const [incidentTypeSec, setIncidentTypeSec] = useState(null);
  const [otherSecIncidentType, setOtherSecIncidentType] = useState("");
  const [involvesChild, setInvolvesChild] = useState({
    value: "no",
    label: "No",
  });
  const [involvesNonClient, setInvolvesNonClient] = useState({
    value: "no",
    label: "No",
  });

  const [
    program,
    setProgram,
    setProgramAutocomplete,
    setProgramShowAutocomplete,
  ] = useSelectFieldInfo();

  const [
    immediateResponse,
    setImmediateResponse,
    setImmediateResponseAutocomplete,
    setImmediateResponseShowAutocomplete,
  ] = useSelectFieldInfo();

  const [staffCompleting, setStaffCompleting] = useState("");
  const [supervisorReviewer, setSupervisorReviewer] = useState("");
  const [dateCompleted, setDateCompleted] = useState(new Date());
  const [modalDisplay, setModalDisplay] = useState("none");

  const {
    incidentTypePri,
    setIncidentTypePri,
    setIncidentTypePriShowAutocomplete,
    incTypesOptions,
    sortedIncTypeOptions,
    updateOptionsFromDescription: updateIncTypesOptions,
  } = useIncTypeOptions();

  const {
    locations,
    programs,
    immediateResponses,
    services,
  } = useFormOptions();

  useAutocomplete({
    description,
    immediateResponses,
    immediateResponse,
    services,
    locations,
    programs,
    clientInitials,
    incTypesOptions,
    setImmediateResponseAutocomplete,
    setServicesInvolvedAutocomplete,
    setLocationAutocomplete,
    setProgramAutocomplete,
    setDateOccurredAutocomplete,
    setClientInitialsAutocomplete,
    setClientSecInitialsAutocomplete,
    updateIncTypesOptions,
  });

  const {
    submitClicked,
    setSubmitClicked,
    submitWarningStyle,
    handleSubmit,
    checkRequiredFields,
  } = useSubmit({
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
  });

  return (
    <div className="App">
      <div
        style={{
          position: "fixed",
          top: "0",
          left: "0",
          width: "100%",
          bottom: "0",
          backgroundColor: "rgba(0,0,0,0.5)",
          zIndex: "10",
          display: modalDisplay,
        }}
      >
        <div
          className="ModalBox"
          style={{
            width: "500px",
            height: "auto",
            backgroundColor: "#fff",
            float: "none",
            margin: "10% auto 0",
            borderRadius: "7px",
            textAlign: "left",
            padding: "20px",
          }}
        >
          <ModalClose onClick={() => setModalDisplay("none")}></ModalClose>
          <div>
            <b>Client Involved - Primary: </b> {clientInitials}
          </div>
          <div>
            <b>Client Involved - Secondary: </b> {clientSecInitials}
          </div>
          <div>
            <b>Location: </b> {location?.label}
          </div>
          <div>
            <b>Location Detail: </b> {locationDetail}
          </div>
          <div>
            <b>Date of Occurrence: </b> {dateOccurred?.toLocaleString()}
          </div>
          <div>
            <b>Services Involved: </b>
            {servicesInvolved?.map((o) => o.label).join(", ")}
          </div>
          <div>
            <b>Other Services Involved: </b> {otherServices}
          </div>
          <div>
            <b>Staff Involved: </b>
            {`${staffInvolvedFirst} ${staffInvolvedLast}`}
          </div>
          <div>
            <b>Incident Type - Primary: </b> {incidentTypePri?.label}
          </div>
          <div>
            <b>Incident Type - Secondary: </b> {incidentTypeSec?.label}
          </div>

          <div>
            <b>Immediate Response: </b>{" "}
            {immediateResponse?.map((o) => o.label).join(", ")}
          </div>

          <div>
            <b>Program: </b> {program?.label}
          </div>

          <div>
            <b>Involves a Child? </b> {involvesChild?.label}
          </div>
          <div>
            <b>Involves a non-client guest? </b> {involvesNonClient?.label}
          </div>

          <div>
            <b>Staff Completing this Report: </b> {staffCompleting}
          </div>
          <div>
            <b>Program Supervisor Reviewer: </b> {supervisorReviewer}
          </div>

          <div style={{ width: "100%", textAlign: "center" }}>
            <input type="submit" value="Submit" onClick={handleSubmit}></input>
          </div>
        </div>
      </div>
      <img src={logo} alt="YW logo"></img>
      <h1>Critical Incident Report Form</h1>
      <h2>Prototype - December 1, 2020 </h2>
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
            setShowAutocomplete={setClientInitialsShowAutocomplete}
            submitClicked={submitClicked}
            customStyle={{ width: "95%" }}
          ></TextInput>
          <TextInput
            label="Client Involved - Secondary (Initials)"
            required={false}
            value={clientSecInitials}
            setValue={setClientSecInitials}
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
          <div style={{ width: "100%" }}>
            <label>Did this incident involve a child?</label>
            <Select
              styles={{
                container: (provided) => ({
                  ...provided,
                  width: "95%",
                }),
              }}
              value={involvesChild}
              onChange={(option) => {
                setInvolvesChild(option);
              }}
              options={[
                { value: "no", label: "No" },
                { value: "yes", label: "Yes" },
              ]}
            ></Select>
          </div>
          <div style={{ width: "100%" }}>
            <label>Did this incident involve a non-client guest?</label>
            <Select
              value={involvesNonClient}
              onChange={(option) => {
                setInvolvesNonClient(option);
              }}
              options={[
                { value: "no", label: "No" },
                { value: "yes", label: "Yes" },
              ]}
            ></Select>
          </div>
        </FormRow>

        <FormRow>
          <SelectInput
            label="Program"
            options={programs}
            value={program}
            setValue={setProgram}
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
        <button onClick={(e) => e.preventDefault()}>Download</button>
      </form>
      <FeedbackBox />;
    </div>
  );
}

export default App;
