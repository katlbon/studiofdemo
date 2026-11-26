import Rail from '../../common/Rail'
import styles from './shipin-tiles.module.scss'

type Tile = {
  image: string
  label: string
  url: string
}

export type ShipinTilesProps = {
  title?: string
  tiles?: Tile[]
}

/**
 * White rounded tiles with an image and an uppercase label underneath.
 * Used for "Lo más buscado" (categories) and "Nuestras marcas" (brands).
 */
export default function ShipinTiles({ title, tiles = [] }: ShipinTilesProps) {
  if (tiles.length === 0) return null

  return (
    <Rail title={title} visible={8} className={styles.tiles}>
      {tiles.map((tile, index) => (
        <a key={`${tile.url}-${index}`} href={tile.url} data-tile>
          <span data-tile-box>
            <img src={tile.image} alt="" loading="lazy" />
          </span>
          <span data-tile-label>{tile.label}</span>
        </a>
      ))}
    </Rail>
  )
}
