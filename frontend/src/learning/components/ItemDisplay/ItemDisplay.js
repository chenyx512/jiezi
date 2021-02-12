import React from 'react';
import PropTypes from 'prop-types';

import CharDisplay from './CharacterDisplay/CharDisplay';
import WordDisplay from './WordDisplay/WordDisplay';
import RadDisplay from './RadicalDisplay/RadDisplay';

import '@learning.styles/ItemDisplay.css';

import { ItemDescriptor } from '@interfaces/CoreItem';

/**
 * Statically display an item (word, character, or radical) 
 * using an ItemDescriptor.
 * @param { ItemDescriptor } props 
 */
export default function ItemDisplay(props) {
    
    const renderSwitch = (type, qid) => {
        switch (type) {
        case 'character':
            return (<CharDisplay qid={qid} />);
        case 'radical':
            return <RadDisplay qid={qid} />;
        case 'word':
            return <WordDisplay qid={qid} />;
        default:
            return ;
        }
    };

    const renderNext = () => {
        if (props.onActionNext != null)
            return (
                <button onClick={props.onActionNext}>
                    next
                </button>
            );
    };

    return (
        <>
            { renderNext() }
            <div className='content-card-container
            box-shadow'>
                { renderSwitch(props.type, props.qid) }
            </div>
        </>
    );
}

ItemDisplay.propTypes = {
    type: PropTypes.string,
    qid: PropTypes.number,
    onActionNext: PropTypes.func
};