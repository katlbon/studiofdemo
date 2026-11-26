import styles from './campaign-banner.module.scss'

export type CampaignBannerProps = {
  desktopImage: string
  mobileImage?: string
  alt?: string
  buttonLabel?: string
  url?: string
}

/** Full-width campaign image (art-directed for mobile) with a centered CTA. */
export default function CampaignBanner({
  desktopImage,
  mobileImage,
  alt = '',
  buttonLabel,
  url = '#',
}: CampaignBannerProps) {
  if (!desktopImage) return null

  return (
    <section className={styles.campaignBanner}>
      <a href={url} data-campaign-link>
        <picture>
          {mobileImage && <source media="(max-width: 767px)" srcSet={mobileImage} />}
          <img src={desktopImage} alt={alt} loading="lazy" />
        </picture>
        {buttonLabel && <span data-campaign-button>{buttonLabel}</span>}
      </a>
    </section>
  )
}
