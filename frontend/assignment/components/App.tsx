import React from 'react';
import AssignmentDisplay from '@assignment.components/AssignmentDisplay';


type Props = {
    action: string,
    content: {qid: number}
}

export default class App extends React.Component<Props> {

    render(): JSX.Element {
        switch (this.props.action) {
        case 'assignment':
            return <AssignmentDisplay {...this.props.content} />;
        case 'search':
            return <SearchPage {...this.props.content} />;
        default:
            return <>something is wrong</>;
        }
    }
}