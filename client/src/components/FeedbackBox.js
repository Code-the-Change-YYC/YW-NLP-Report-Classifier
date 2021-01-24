import React from 'react'
import styled from 'styled-components';

const FeedbackBoxWrapper = styled.div`
  margin-top: 20px;
  padding: 10px 100px;
  text-align: center;
  background-color: #49ace9;
  display: inline-block;
`;


const FeedbackBox = () => (
      <FeedbackBoxWrapper>
        Please provide us feedback at: <br></br>
        <a href="https://forms.gle/NxvkQafJ3h5osQDD8">
          https://forms.gle/NxvkQafJ3h5osQDD8
        </a>
      </FeedbackBoxWrapper>
);

export default FeedbackBox;