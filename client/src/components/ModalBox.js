import React, { useState } from "react";
import "../App.css";
import { ModalClose } from "../styled";

const ModalBox = ({
    formData: {
        clientInitials,
        clientSecInitials,
        location,
        locationDetail,
        dateOccurred,
        servicesInvolved,
        otherServices,
        staffInvolvedFirst,
        staffInvolvedLast,
        incidentTypePri,
        incidentTypeSec,
        immediateResponse,
        program,
        involvesChild,
        involvesNonClient,
        staffCompleting,
        supervisorReviewer,
    },
    modalDisplay,
    setModalDisplay,
    handleSubmit,
}) => {
    const [loading, setLoading] = useState(false);
    return (
        <div className="ModalContainer" style={{ display: modalDisplay }}>
            <div className="ModalBox">
                <ModalClose
                    className="ModalClose"
                    onClick={() => setModalDisplay("none")}
                ></ModalClose>
                <div className="ModalContent">
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
                        <b>Date of Occurrence: </b>{" "}
                        {dateOccurred?.toLocaleString()}
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
                        <b>Incident Type - Primary: </b>{" "}
                        {incidentTypePri?.label}
                    </div>
                    <div>
                        <b>Incident Type - Secondary: </b>{" "}
                        {incidentTypeSec?.label}
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
                        <b>Involves a non-client guest? </b>{" "}
                        {involvesNonClient?.label}
                    </div>

                    <div>
                        <b>Staff Completing this Report: </b> {staffCompleting}
                    </div>
                    <div>
                        <b>Program Supervisor Reviewer: </b>{" "}
                        {supervisorReviewer}
                    </div>
                </div>

                <div
                    className="ModalSubmit"
                    style={{ width: "100%", textAlign: "center" }}
                >
                    <input
                        type="submit"
                        value="Submit"
                        onClick={(e) => {
                            setLoading(true);
                            handleSubmit(e);
                        }}
                    ></input>
                    <div
                        className="loadingText"
                        style={{ display: loading ? "block" : "none" }}
                    >
                        <b>Redirecting...</b>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ModalBox;
