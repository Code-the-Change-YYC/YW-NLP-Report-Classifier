import styled from 'styled-components';

export const FormRow = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  textarea {
    align-self: stretch;
    font-size: 12pt;
  }

  & > label {
    margin-bottom: 5px;
  }

  & > div > label {
    display: flex;
    margin-bottom: 5px;
  }

  margin: 5px 0px;
  text-align: left;
`;

export const Input = styled.input`
  padding: 8px 5px;
  font-size: 12pt;
  border: 1px solid lightgray;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
`;

export const Textarea = styled.textarea`
  padding: 8px 5px;
  font-size: 12pt;
  border: 1px solid lightgray;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
`;

export const HR = styled.hr`
  margin: 20px 30px 20px;
`;

export const ModalClose = styled.div`
  float: right;
  text-align: right;
  cursor: pointer;
  line-height: 10px;

  &:before {
    content: "x";
    color: #ff0000;
    font-weight: normal;
    font-family: Arial, sans-serif;
    font-size: 30px;
  }
`;
