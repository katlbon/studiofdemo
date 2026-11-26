import { Image_unstable as Image } from '@faststore/core/experimental'

import styles from './image-banner.module.scss'

export type ImageBannerProps = {
  image: {
    src: string
    alt?: string
  }
  url?: string
  linkTargetBlank?: boolean
}

/** Thin full-width promotional image strip (e.g. payment or shipping promo). */
export default function ImageBanner({
  image,
  url,
  linkTargetBlank,
}: ImageBannerProps) {
  if (!image?.src) {
    return null
  }

  const img = (
    <Image
      src={image.src}
      alt={image.alt ?? ''}
      width={1280}
      height={160}
      sizes="100vw"
      data-image-banner-image
    />
  )

  return (
    <section className={`section ${styles.imageBanner}`}>
      <div className="layout__content">
        {url ? (
          <a
            href={url}
            target={linkTargetBlank ? '_blank' : undefined}
            rel={linkTargetBlank ? 'noopener noreferrer' : undefined}
          >
            {img}
          </a>
        ) : (
          img
        )}
      </div>
    </section>
  )
}
