// Randomly style
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
        marginTop: '15%',
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
        fontSize: 16,
        fontWeight: 700,
    }]
}

export const InputStyle = {
    marginHorizontal: 30,
    marginVertical: 15,
    paddingVertical: 15,
    paddingHorizontal: 8,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#000000',
    borderRadius: 5,
    color: '#000000',
}

export const BoundingBoxStyle = (x, y, width, height) => {
    return {
        position: 'absolute',
        left: x,
        top: y,
        width: width,
        height: height,
        borderWidth: 2,
        borderColor: '#00FF00',
        borderRadius: 5,
    }
}