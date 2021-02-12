interface ReviewQuestion {
    id: String,
    form: String,
    content: ReviewQuestionContent
}

interface ReviewQuestionContent {
    question: TextProvider,
}

export interface MCQuestionContent extends ReviewQuestionContent {
    context: TextProvider,
    choices: [TextProvider]
}

export interface CNDQuestionContent extends ReviewQuestionContent {
    title: TextProvider,
    answer_length: TextProvider,
    choices: [TextProvider]
}

export interface FITBQuestionContent extends ReviewQuestionContent {
    title: TextProvider
}

export interface ReviewQuestionDescriptor {
    qid: Number,
    hasNext: Boolean,
    onActionNext: Function
}

interface TextProvider {
    text: String,
    audio: String
}

export default ReviewQuestion;