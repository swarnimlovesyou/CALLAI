"use client"

import type React from "react"

import { createContext, useContext, useEffect, useState } from "react"
import { useRouter, usePathname } from "next/navigation"
import { useToast } from "@/components/ui/use-toast"
import { getApi, mockApi } from "@/lib/api"

type User = {
  id: number
  username: string
  first_name: string
  last_name: string
}

type AuthContextType = {
  user: User | null
  token: string | null
  login: (username: string, password: string) => Promise<boolean> // Updated to return a boolean
  logout: () => void
  isLoading: boolean
  isAuthenticated: boolean // Added helper property
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()
  const pathname = usePathname()
  const { toast } = useToast()
  const api = getApi()

  const isAuthenticated = !!token && !!user // Added isAuthenticated property

  useEffect(() => {
    // Check if we have a token in localStorage
    const storedToken = localStorage.getItem("auth_token")
    const storedUser = localStorage.getItem("auth_user")

    if (storedToken && storedUser) {
      setToken(storedToken)
      setUser(JSON.parse(storedUser))
      validateToken(storedToken) // Validate token on initial load
    }

    setIsLoading(false)
  }, [])

  const validateToken = async (token: string) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
      const response = await fetch(`${apiUrl}/api/agents/me/`, {
        headers: {
          Authorization: `Token ${token}`,
          Accept: "application/json",
        },
        mode: "cors",
      })

      if (!response.ok) {
        logout() // Token is invalid, log the user out
      }
    } catch (error) {
      console.error("Token validation error:", error)
    }
  }

  useEffect(() => {
    // Redirect logic
    if (!isLoading) {
      const publicPaths = ["/login", "/"]
      const isPublicPath = publicPaths.includes(pathname)

      if (!token && !isPublicPath) {
        router.push("/login")
      } else if (token && pathname === "/login") {
        router.push("/dashboard")
      }
    }
  }, [token, pathname, isLoading, router])

  const login = async (username: string, password: string): Promise<boolean> => {
    setIsLoading(true)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
      console.log("Login attempt using API URL:", apiUrl)

      const response = await fetch(`${apiUrl}/api/token-auth/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
        body: JSON.stringify({ username, password }),
        mode: 'cors',
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        console.error("Login response error:", response.status, errorData)
        throw new Error(errorData.detail || `Login failed with status: ${response.status}`)
      }

      const data = await response.json()
      const authToken = data.token

      // Fetch user details with the token
      const userResponse = await fetch(`${apiUrl}/api/agents/me/`, {
        headers: {
          "Authorization": `Token ${authToken}`,
          "Accept": "application/json",
        },
        mode: 'cors',
      })

      if (!userResponse.ok) {
        console.error("User details response error:", userResponse.status)
        throw new Error(`Failed to fetch user details: ${userResponse.status}`)
      }

      const userData = await userResponse.json()

      // Save to state and localStorage
      setToken(authToken)
      setUser(userData)
      localStorage.setItem("auth_token", authToken)
      localStorage.setItem("auth_user", JSON.stringify(userData))

      toast({
        title: "Login successful",
        description: `Welcome back, ${userData.user?.first_name || userData.first_name || username}!`,
      })

      router.push("/dashboard")
      return true // Return true on successful login
    } catch (error) {
      console.error("Login error details:", error)
      toast({
        title: "Login failed",
        description: error instanceof Error ? error.message : "Please check your credentials and try again.",
        variant: "destructive",
      })
      return false // Return false on failed login
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem("auth_token")
    localStorage.removeItem("auth_user")
    router.push("/login")
    toast({
      title: "Logged out",
      description: "You have been successfully logged out.",
    })
  }

  return <AuthContext.Provider value={{ user, token, login, logout, isLoading, isAuthenticated }}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}

