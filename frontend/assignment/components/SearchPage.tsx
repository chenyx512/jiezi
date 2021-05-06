import React, {useState, useRef} from 'react';
import styled from 'styled-components';
import '@assignment.styles/SearchPage.css';
import HeaderView from '@assignment.components/HeaderView';

// Containers
const ContentContainer = styled.div`
    max-width: 900px;
    margin: 20px auto;
    
    @media only screen and (max-width: 480px) {
    margin: 20px 0;
    }
`;
const SearchButton = styled.button`
    width: 100px;
    height: 20px;
    margin-left: auto;
    margin-right: auto;
    border-radius: 10px;
    background-color: red;
    font-size: 1.5rem;
    text-align: center;
    color: white;
    outline: none;
    box-shadow: none;
`;

const ChoiceButton = styled.button`
    width: 100px;
    height: 20px;
    margin-left: auto;
    margin-right: auto;
    border-radius: 10px;
    border: none;
    font-size: 1.5rem;
    text-align: center;
    color: black;
    outline: none;
    box-shadow:none;
`;

const SearchPage = (props: Props): JSX.Element => {
    const Search // = needed backup updates
    const [chinese, setChinese] = useState<boolean>(false);
    const [pinyin, setPinyin] = useState<boolean>(false);
    const [english, setEnglish] = useState<boolean>(false);
    const displayRef = useRef<HTMLDivElement>(null);



    const renderSearch = (search: Search) => {
        return (
            <ContentContainer>
                <SearchButton>Search</SearchButton>
                <div className = {'search-choice-container'}>
                    <ChoiceButton onclick={setPinyin(true)}>Pinyin</ChoiceButton>
                    <ChoiceButton onclick={setChinese(true)}>Chinese</ChoiceButton>
                    <ChoiceButton onclick={setEnglish(true)}>English</ChoiceButton>
                </div>
                <ul>
                    {%for i in Search%}
                        <li>{obj.chinese}</li>
                    {%end for%}
                </ul>
            </ContentContainer>
        );
    };

    if (Search === null)
        return (<>searching</>);
    else
        return renderSearch(Search);
};

export default SearchPage;
