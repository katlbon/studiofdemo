import styles from './search-bar.module.scss'

export type SearchBarProps = {
  placeholder?: string
}

/**
 * Full-width search pill shown under the header on mobile and tablet.
 * Submits a plain GET form to the store's search page (/s?q=...).
 */
export default function SearchBar({
  placeholder = 'What are you looking for?',
}: SearchBarProps) {
  return (
    <section className={`section ${styles.searchBar}`}>
      <div className="layout__content">
        <form action="/s" method="get" role="search" data-search-bar-form>
          <button type="submit" aria-label="Search" data-search-bar-button>
            <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true">
              <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" strokeWidth="2" />
              <path d="M20 20l-4-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
          </button>
          <input
            type="search"
            name="q"
            required
            placeholder={placeholder}
            aria-label={placeholder}
            data-search-bar-input
          />
        </form>
      </div>
    </section>
  )
}
