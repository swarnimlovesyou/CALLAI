import { useEffect, useState } from "react"

export function useDarkReader() {
  const [isDarkReaderActive, setIsDarkReaderActive] = useState(false)

  useEffect(() => {
    const checkDarkReader = () => {
      setIsDarkReaderActive(!!window.matchMedia?.(`(prefers-color-scheme: dark)`).matches)
    }

    checkDarkReader()
    
    // Listen for changes
    const darkReaderObserver = new MutationObserver(checkDarkReader)
    darkReaderObserver.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    })

    return () => darkReaderObserver.disconnect()
  }, [])

  return isDarkReaderActive
}
