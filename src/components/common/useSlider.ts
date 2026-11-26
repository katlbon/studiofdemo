import { useCallback, useEffect, useRef, useState } from 'react'

/**
 * Minimal scroll-snap slider state: tracks the visible slide from scroll
 * position, exposes goTo(), and optionally autoplays (paused on hover/focus).
 */
export function useSlider(count: number, autoplayMs = 0) {
  const trackRef = useRef<HTMLDivElement>(null)
  const [active, setActive] = useState(0)
  const [paused, setPaused] = useState(false)

  const goTo = useCallback(
    (index: number) => {
      const track = trackRef.current
      if (!track || count === 0) return
      const next = (index + count) % count
      track.scrollTo({ left: next * track.clientWidth, behavior: 'smooth' })
    },
    [count]
  )

  useEffect(() => {
    const track = trackRef.current
    if (!track) return

    const onScroll = () => {
      const width = track.clientWidth || 1
      setActive(Math.round(track.scrollLeft / width))
    }

    track.addEventListener('scroll', onScroll, { passive: true })
    return () => track.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    if (!autoplayMs || paused || count < 2) return
    const timer = window.setInterval(() => goTo(active + 1), autoplayMs)
    return () => window.clearInterval(timer)
  }, [active, autoplayMs, count, goTo, paused])

  const pauseProps = {
    onMouseEnter: () => setPaused(true),
    onMouseLeave: () => setPaused(false),
    onFocus: () => setPaused(true),
    onBlur: () => setPaused(false),
  }

  return { trackRef, active, goTo, pauseProps }
}
