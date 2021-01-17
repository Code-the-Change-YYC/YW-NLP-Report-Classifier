import { useFormOptions } from "./useFormOptions";
import { useIncTypeOptions } from "./useIncTypeOptions";
import React, { useState, useCallback, useEffect } from "react";
import logo from "./logo.jpg";
import "./App.css";
import _ from "lodash";
import chrono from "chrono-node";
import Select from "react-select";
import { getRedirectUrl } from "./actions/submit";
import { FormRow, Input, Textarea, HR, ModalClose } from "./styled";
import TextInput from "./components/TextInput";
import useTextFieldInfo from "./hooks/useTextFieldInfo";
import useSelectFieldInfo from "./hooks/useSelectFieldInfo";
import useDateFieldInfo from "./hooks/useDateFieldInfo";
import SelectInput from "./components/SelectInput";
import DateInput from "./components/DateInput";
import ReactDatePicker from "react-datepicker";
import styled from "styled-components";

const FeedbackBox = styled.div`
  margin-top: 20px;
  padding: 10px 100px;
  text-align: center;
  background-color: #49ace9;
  display: inline-block;
`;

const IncTypeOption = ({ confidence, label }) => {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        width: "100%",
      }}
    >
      <div>{label}</div>
      <div style={{ marginLeft: "15px", color: "#999999" }}>{confidence}</div>
    </div>
  );
};

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
    updateOptionsFromDescription: updateIncTypesOptions,
  } = useIncTypeOptions();

  const {
    locations,
    programs,
    immediateResponses,
    services,
  } = useFormOptions();

  const [submitClicked, setSubmitClicked] = useState(false);

  useEffect(() => {
    if (!immediateResponse || immediateResponse?.length === 0) {
      const otherImmediateResponse = immediateResponses?.find((response) => {
        if (response?.value) {
          return response.value.toLowerCase().includes("other");
        }
      });
      setImmediateResponseAutocomplete((prev) =>
        otherImmediateResponse ? [otherImmediateResponse] : prev
      );
    }
  }, [immediateResponses, immediateResponse, setImmediateResponseAutocomplete]);

  // Checking functions
  // These functions are run when the description updates and contain the logic
  // for autocompleting the form fields.

  const autocompleteSingleOption = (options) => {
    const lowercasedDescription = description.toLowerCase();
    return options.find((option) =>
      (option.keywords || []).some((keyword) =>
        lowercasedDescription.includes(keyword.toLowerCase())
      )
    );
  };

  const autocompleteMultipleOptions = (options) => {
    const lowercasedDescription = description.toLowerCase();
    const newOptions = options.filter((option) =>
      (option.keywords || []).some((keyword) =>
        lowercasedDescription.includes(keyword.toLowerCase())
      )
    );
    return newOptions;
  };

  const checkServices = () => {
    if (services) {
      setServicesInvolvedAutocomplete(autocompleteMultipleOptions(services));
    }
  };

  const checkLocation = () => {
    if (locations) {
      setLocationAutocomplete(autocompleteSingleOption(locations));
    }
  };

  const checkProgram = () => {
    if (programs) {
      setProgramAutocomplete(autocompleteSingleOption(programs));
    }
  };

  const checkImmediateResponse = () => {
    if (immediateResponses) {
      setImmediateResponseAutocomplete(
        autocompleteMultipleOptions(immediateResponses)
      );
    }
  };

  const checkDate = () => {
    const results = chrono.parse(description);

    if (results && results.length) {
      let date = results[0].start.date();
      if (date > Date.now()) {
        date = new Date();
      }
      setDateOccurredAutocomplete(date);
    }
  };

  const checkInitials = () => {
    const found = description.match(/\b(?!AM|PM)([A-Z]{2})\b/g);
    if (found && found.length) {
      setClientInitialsAutocomplete(found[0]);
    } else {
      setClientInitialsAutocomplete("");
    }
  };

  const checkRequiredFields = () => {
    return (
      description.length > 0 &&
      clientInitialsValid &&
      location !== undefined &&
      incidentTypePri !== undefined &&
      program !== undefined &&
      immediateResponse.length > 0 &&
      staffCompleting.length > 0 &&
      supervisorReviewer.length > 0 &&
      dateOccurred !== null &&
      dateCompleted !== null
    );
  };

  const warningStyle = (val) => {
    if (
      submitClicked &&
      (val === null || val === undefined || val.length === 0)
    ) {
      return { border: "1px solid red" };
    }
    return {};
  };

  const checkSecondInitials = () => {
    const found = description.match(/\b(?!AM|PM)([A-Z]{2})\b/g);
    if (found && found.length) {
      for (const match of found) {
        if (match !== clientInitials) {
          setClientSecInitialsAutocomplete(match);
          return;
        }
      }
    }
    setClientSecInitials("");
  };

  // run this 1000 seconds when the description is updated
  const onDescriptionUpdate = useCallback(
    _.throttle(() => {
      checkLocation();
      checkInitials();
      checkSecondInitials();
      checkServices();
      checkDate();
      updateIncTypesOptions(description);
      checkProgram();
      checkImmediateResponse();
    }, 1000),
    [checkLocation, checkInitials, checkServices, checkDate, _]
  );

  useEffect(onDescriptionUpdate, [description]);

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
      occurence_time: dateOccurred,
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
  };

  const sortedIncTypeOptions = incTypesOptions?.sort((firstEl, secondEl) => {
    if (firstEl.confidence && secondEl.confidence) {
      return (
        Number.parseFloat(secondEl.confidence) -
        Number.parseFloat(firstEl.confidence)
      );
    }
  });

  const numConfidenceValues = 5;
  const reactSelectIncTypeOpts = sortedIncTypeOptions?.map((opt, i) => {
    if (i > numConfidenceValues - 1) {
      return {
        ...opt,
        confidence: "",
      };
    } else {
      return opt;
    }
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
          style={{ ...warningStyle(description) }}
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
            noFutureDate
          ></DateInput>
        </FormRow>

        <FormRow style={{ flexDirection: "row" }}>
          <SelectInput
            label="Incident Type (Primary)"
            value={incidentTypePri}
            options={reactSelectIncTypeOpts}
            setValue={setIncidentTypePri}
            setShowAutocomplete={setIncidentTypePriShowAutocomplete}
            submitClicked={submitClicked}
            formatOptionLabel={IncTypeOption}
            required
            customStyle={{ width: "95%" }}
          ></SelectInput>

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
              style={{ width: "95%", ...warningStyle(staffCompleting) }}
            ></Input>
          </div>
          <div style={{ width: "100%" }}>
            <label>Name of Program Supervisor Reviewer *</label>
            <Input
              value={supervisorReviewer}
              onChange={(e) => setSupervisorReviewer(e.target.value)}
              style={{ ...warningStyle(supervisorReviewer) }}
            ></Input>
          </div>
        </FormRow>
        <FormRow>
          <label>Completed On *</label>
          <ReactDatePicker
            selected={dateCompleted}
            showTimeSelect
            timeIntervals={15}
            dateFormat="MMMM d, yyyy h:mm aa"
            setDate={setDateCompleted}
            value={Date.now()}
            onChange={(date) => {
              if (date > Date.now()) {
                setDateCompleted(new Date());
              } else {
                setDateCompleted(date);
              }
            }}
            maxDate={new Date()}
            minTime={new Date().setHours(0, 0, 0, 0)}
            maxTime={new Date()}
            customInput={<Input></Input>}
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
      <FeedbackBox>
        Please provide us feedback at: <br></br>
        <a href="https://forms.gle/NxvkQafJ3h5osQDD8">
          https://forms.gle/NxvkQafJ3h5osQDD8
        </a>
      </FeedbackBox>
    </div>
  );
}

export default App;
