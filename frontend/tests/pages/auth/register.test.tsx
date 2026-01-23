import React from 'react'
import { render } from '@testing-library/react'
import Register from '@/pages/auth/register'

jest.mock('next/router', () => require('next-router-mock'))
jest.mock('react-hot-toast')
jest.mock('@/lib/auth', () => ({
  useAuth: () => ({
    register: jest.fn(),
    user: null,
  }),
}))

describe('Register Page', () => {
  it('renders without crashing', () => {
    const { container } = render(<Register />)
    expect(container).toBeTruthy()
  })
})
