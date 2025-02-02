import React from "react";
import styled from "styled-components";

import "@learning.styles/ItemDisplay.css";
import ItemPhonetic from "../ItemPhonetic";

const ContainerDefinition = styled.div`
  // display: flex;
  justify-content: start;
  align-items: center;
  width : auto;
  max-width: 1000px;
  @media only screen and (max-width: 800px) {
    flex-direction: column;
  }
`;

const TableContainer = styled.div`
  // margin-left: 15px;
  width: auto;
  height: auto
  width: 70%;
  max-width: 200px;
  max-height: 4.5em;
`;

const DefinitionList = styled.ul`
  display: inline-block;
  padding-left: 0px;
  font-size: 1.2em;
  // width: fit-content;
  margin-right: 1vmin;
  max-height: 80px;
  overflow: overlay;
`;

// const DefinitionList = styled.ul`

//     padding-left: 70px;
//     font-size: 1.3em;

//     @media only screen and (max-width: 480px) {
//         padding: 0;
//     }
// `;

const ListTitle = styled.i`
  font-size: 0.6em;
  font-style: normal;
  color: var(--teritary-text);
  line-height: 1em;
`;

const ListItem = styled.li`
  line-height: 1.3em;
  text-overflow: ellipsis;
`;

type Props = {
  /** The character in chinese */
  chinese: string;

  /** Resource URL of the audio pronunciation */
  audioURL: string;

  /** Pronunciation in pinyin */
  pinyin: string;

  /** The definitions to be displayed */
  definitions: string[];
};

const CharDefinition = (props: Props): JSX.Element => {
  return (
    // <ContainerDefinition>
    <>
      <ItemPhonetic
        item={props.chinese}
        pinyin={props.pinyin}
        audioURL={props.audioURL}
        useStroke={true}
        type="character"
      />
      <TableContainer className="divider">
        <DefinitionList>
          {/* <ListTitle>Definitions:</ListTitle> */}
          {props.definitions.map((elem, i) => {
            return (
              <ListItem key={i} className="use-serifs">
                {elem}
              </ListItem>
            );
          })}
        </DefinitionList>
      </TableContainer>
    </>
    // </ContainerDefinition>
  );
};

export default CharDefinition;
