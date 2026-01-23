import '@testing-library/jest-dom'

jest.mock('next/router', () => require('next-router-mock'))

global.fetch = jest.fn()
