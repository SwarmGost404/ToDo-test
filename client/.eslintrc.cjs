module.exports = {
  extends: [
    'plugin:vue/vue3-recommended',
    'eslint:recommended',
    'prettier'
  ],
  plugins: ['prettier'],
  rules: {
    'prettier/prettier': ['error', {}, { usePrettierrc: true }]
  }
}