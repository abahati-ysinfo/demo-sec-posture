import React from 'react'
import { render } from '@testing-library/react'
import Login from '@/pages/auth/login'

jest.mock('next/router', () => require('next-router-mock'))
jest.mock('react-hot-toast')
jest.mock('@/lib/auth', () => ({
  useAuth: () => ({
    login: jest.fn(),
    user: null,
  }),
}))

describe('Login Page', () => {
  it('renders without crashing', () => {
    const { container } = render(<Login />)
    expect(container).toBeTruthy()
  })
})
