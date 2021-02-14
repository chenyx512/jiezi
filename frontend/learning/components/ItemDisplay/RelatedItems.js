import React from 'react';
import styled from 'styled-components';
import PropTypes, { object } from 'prop-types';

import '@learning.styles/ItemDisplay.css';

const Heading = styled.h2`
    color: var(--teritary-text);
    margin-top: 10px;
    font-size: 0.9em;
    font-weight: 400;
`;

const RelatedItemsList = styled.ul`
    line-height: 1.5em;
`;

/** Display related words that a user has seen. */
export default class RelatedItems extends React.Component {

    static propTypes = {
        /** The character used to look up related items
         * a user has viewed so far. */
        item: PropTypes.string.isRequired,

        // 'items' is an array of objects 
        items: PropTypes.arrayOf(object),

        /** The type of the related items to be displayed
         * (word or character) */
        itemType: PropTypes.oneOf(['word', 'character']).isRequired
    }



    render() {
        const items = this.props.items;
        if (items.length == 0) {
            return <></>;
        } else {
            return (
                <>
                    <Heading>
                        {`Related ${this.props.itemType}s you've seen`}
                    </Heading>
                    <RelatedItemsList>
                        {items.map((v, i) => {
                            return (<RelatedItemEntry
                                style={i % 2 ? {background: '#F9F9F9'} : {}}
                                key={v.chinese}
                                item={v}
                            />);
                        })}
                    </RelatedItemsList>
                </>
            );
        }
    }
}

const RelatedWordItemDisplay = styled.li`
    display: flex;
    justify-content: flex-start;
    padding: 3px 3px 3px 6px;
`;

const ItemComp = styled.p`
    display: inline-block;
    font-size: 1em;
    color: var(--secondary-text);
    padding-right: 15px;
    margin-bottom: 0;
    white-space: nowrap;
`;

const ItemCompWord = styled(ItemComp)`
    font-size: 1.2em;
`;

const ItemCompPhonetic = styled(ItemComp)`
    font-size: 0.9em;
`;

const ItemCompDef = styled(ItemComp)`
    flex-grow: 3;
    max-width: 75%;
    margin-left: auto;
    text-overflow: ellipsis;
    overflow: hidden;
`;//
class RelatedItemEntry extends React.Component {

    static propTypes = {
        item: PropTypes.object,
        style: PropTypes.object
    }

    render() {
        const {chinese, pinyin, fullDefinition} = this.props.item;

        // TODO: The curly font for part of speech
        return (
            <RelatedWordItemDisplay style={this.props.style} >
                <ItemCompWord className='use-chinese'>
                    {chinese}
                </ItemCompWord>
                <ItemCompPhonetic className='use-chinese'>
                    {`/${pinyin}/`}
                </ItemCompPhonetic>
                <ItemCompDef className='use-serifs'>
                    {fullDefinition}
                </ItemCompDef>
            </RelatedWordItemDisplay>
        );
    }
}