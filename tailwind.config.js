/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/templates/**/*.{html,js}"], theme: {
        extend: {
            maxWidth: {
                xxs: "18rem", lxxs: "15rem",
            }, colors: {
                main: "rgb(77, 68, 139)",
                btnblue:"rgb(168, 242, 254)",
                btnpurple:"rgb(77, 70, 140)",
                primary: {
                    DEFAULT: '#662D94',
                    50: '#DBC4ED',
                    100: '#D1B4E8',
                    200: '#BE95DF',
                    300: '#AB75D5',
                    400: '#9856CC',
                    500: '#843ABF',
                    600: '#662D94',
                    700: '#492069',
                    800: '#2B133E',
                    900: '#0D0613',
                    950: '#000000'
                }, secondary: {
                    DEFAULT: '#2F30D5',
                    50: '#C8C8F4',
                    100: '#B7B7F0',
                    200: '#9595EA',
                    300: '#7374E3',
                    400: '#5152DC',
                    500: '#2F30D5',
                    600: '#2223AA',
                    700: '#19197B',
                    800: '#0F104C',
                    900: '#06061E',
                    950: '#010106'
                },
            }, screens: {
                sm: "420px",

                md: "640px",

                lg: "768px",

                xlg: "900px",

                xl: "1180px",

                "2xl": "1280px",

                "3xl": "1536px",

            }, animation: {
                'infinite-scroll': 'infinite-scroll 25s linear infinite',
            }, keyframes: {
                'infinite-scroll': {
                    from: {transform: 'translateX(0)'}, to: {transform: 'translateX(-100%)'},
                }
            }, fontFamily: {
                AnjomanMax_Thin: ["AnjomanMax-Thin"], 
                AnjomanMax_ExLight: ["AnjomanMax_ExLight"],
                AnjomanMax_Light: ["AnjomanMax_Light"],
                AnjomanMax_Medium: ["AnjomanMax-Medium"],
                AnjomanMax_SemiBold: ["AnjomanMax_SemiBold"],
                AnjomanMax_ExBold: ["AnjomanMax_ExBold"],
                AnjomanMax_ExBold: ["AnjomanMax_ExBold"],
                AnjomanMax_Black: ["AnjomanMax_Black"],
                AnjomanMax_Bold: ["AnjomanMax_Bold"],
                AnjomanMax_Regular: ["AnjomanMax_Regular"],
            }, container: {
                center: true,
            },
        },
    }, plugins: [require('tailwindcss-animated')],
}