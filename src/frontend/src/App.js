import React, { useEffect, useState } from "react";
import styled from "styled-components";

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
`;

const Item = styled.div`
  width: 400px;
  padding: 12px;
  margin: 12px 0;
  border: 1px solid red;
`;

const Ad = ({ name, price, description, url }) => {
  return (
    <Item>
      <p>{name}</p>
      <p>{description}</p>
      <p>{price + "€"}</p>
      <a href={url} target="_blank" rel="noreferrer">
        go to website.
      </a>
    </Item>
  );
};

function App() {
  const [state, setState] = useState([]);

  useEffect(() => {
    const updateState = async () => {
      const res = await fetch(process.env.REACT_APP_BACKEND_URL, {
        method: "GET",
        mode: "cors",
      });

      if (res.status === 200) {
        const json = await res.json();
        setState(json);
      }
    };

    updateState();
  }, []);

  return (
    <Wrapper>
      {state.map(({ name, price, description, url }) => (
        <Ad name={name} price={price} description={description} url={url} />
      ))}
    </Wrapper>
  );
}

export default App;
