export const TextStyle = {
    base: {
        fontStyle: 'normal',
        textAlign: 'center',
        color: '#000000',
    },
    hyperlink: [this.base, {
        color: '#0E64D2',
        textDecorationLine: 'underline',
    }],
};

export const TitleStyle = {
    container: {
        marginTop: '12.5%',
    },
    text: [TextStyle.base, {
        fontSize: 24,
        fontWeight: 700,
        color: '#0E64D2',
    }]
}

export const ButtonStyle = {
    container: {
        marginVertical: 15,
        marginHorizontal: 30,
        backgroundColor: '#0E64D2',
        borderRadius: 5,
        paddingVertical: 15,
    },
    text: [TextStyle.base, {
        color: '#FFFFFF',
        fontSize: 14,
        fontWeight: 700,
    }]
}