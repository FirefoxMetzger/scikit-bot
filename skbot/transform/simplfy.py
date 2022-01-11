from typing import List
from .base import CompundLink, Link, InvertLink
from .affine import AffineCompound, Translation, Rotation
from .joints import Joint
import numpy as np


def simplify_links(
    links: List[Link],
    *,
    keep_links: List[Link] = None,
    keep_joints: bool = False,
    eps: float = 1e-16
) -> List[Link]:
    """Simplify a transformation sequence.

    .. currentmodule:: skbot.transform

    This function attempts to optimize the given transformation sequence by
    reducing the number of transformations involved. For this it may replace or
    modify any link in the sequence with the exception of those listed in
    ``keep_links``. Concretely it does the following modifications:

    - It (recursively) flattens :class:`CompoundLinks <CompundLink>`.
    - It replaces double inversions with the original link.
    - It drops 0 degree :class:`Rotations <Rotation>` (identities).
    - It drops 0 amount :class:`Translations <Translation>` (identities).
    - It combines series of translations into a single translation.
    - It sorts translations before rotations.

    .. versionadded:: 0.10.0

    Parameters
    ----------
    links : List[Link]
        The list of links to simplify.
    keep_links : List[Link]
        A list list of links that - if present - should not be simplified.
    keep_joints : bool
        If True treat tf.Joint instances as if they were in keep_links.
    eps : float
        The number below which angles and translations are interpreted as 0.
        Defaults to ``1e-16``.

    Returns
    -------
    improved_links : List[Link]
        A new list of links that is a simplified version of the initial list.
    """

    if keep_links is None:
        keep_links = list()

    def simplify(links: List[Link]) -> List[Link]:
        improved_links: List[Link] = list()

        for idx in range(len(links)):
            link = links[idx]

            # skip if link should not be modified
            if link in keep_links or (isinstance(link, Joint) and keep_joints):
                improved_links.append(link)
                continue

            # resolve inversions
            if isinstance(link, InvertLink):
                inverted_link = link._forward_link

                # still don't touch keep links
                if inverted_link in keep_links or (
                    isinstance(inverted_link, Joint) and keep_joints
                ):
                    improved_links.append(link)
                    continue

                # double inverse
                if isinstance(inverted_link, InvertLink):
                    improved_links.append(inverted_link._forward_link)
                    continue

                # inverted compound link
                if isinstance(inverted_link, (CompundLink, AffineCompound)):
                    for sub_link in reversed(inverted_link._links):
                        improved_links.append(InvertLink(sub_link))
                    continue

                # inverted translation
                if isinstance(inverted_link, Translation):
                    resolved = Translation(
                        inverted_link.direction,
                        amount=-inverted_link.amount,
                        axis=inverted_link._axis,
                    )
                    improved_links.append(resolved)
                    continue

                # inverted rotation
                if isinstance(inverted_link, Rotation):
                    angle = inverted_link.angle
                    resolved = Rotation(
                        inverted_link._u,
                        inverted_link._u_ortho,
                        axis=inverted_link._axis,
                    )
                    resolved.angle = -angle
                    improved_links.append(resolved)
                    continue

            # unpack compound links
            if isinstance(link, (CompundLink, AffineCompound)):
                for sub_link in link._links:
                    improved_links.append(sub_link)
                continue

            # drop identity translations
            if isinstance(link, Translation) and abs(link.amount) < eps:
                continue

            # drop identity rotations
            if isinstance(link, Rotation) and abs(link.angle) < eps:
                continue

            # no improvements for this link
            improved_links.append(link)

        if len(improved_links) != len(links):
            improved_links = simplify(improved_links)
        elif any([a != b for a, b in zip(links, improved_links)]):
            improved_links = simplify(improved_links)

        return improved_links

    def combine_translations(links: List[Link]) -> List[Link]:
        improved_links: List[Link] = list()

        idx = 0
        while idx < len(links):
            link = links[idx]

            if not isinstance(link, Translation):
                improved_links.append(link)
                idx += 1
                continue

            translations: List[Translation] = list()
            for sub_link in links[idx:]:
                if not isinstance(sub_link, Translation):
                    break

                translations.append(sub_link)

            new_direction = np.zeros(link.parent_dim)
            for sub_link in translations:
                new_direction += sub_link.amount * sub_link.direction

            improved_links.append(Translation(new_direction))
            idx += len(translations)

        return improved_links

    def sort_links(links: List[Link]) -> List[Link]:
        improved_links: List[Link] = [x for x in links]

        repeat = True
        while repeat:
            repeat = False
            for idx in range(len(improved_links) - 1):
                link = improved_links[idx]
                next_link = improved_links[idx + 1]

                if isinstance(link, Rotation) and isinstance(next_link, Translation):
                    vector = next_link.amount * next_link.direction
                    vector = link.__inverse_transform__(vector)

                    improved_links[idx + 1] = improved_links[idx]
                    improved_links[idx] = Translation(vector)

                    repeat = True
                    continue

        return improved_links

    improved_links = simplify(links)

    subchains: List[List[Link]] = list()
    keepsies: List[Link] = list()
    current_subchain: List[Link] = list()
    for link in improved_links:
        if link in keep_links or (isinstance(link, Joint) and keep_joints):
            keepsies.append(link)
            subchains.append(current_subchain)
            current_subchain = list()
        else:
            current_subchain.append(link)
    subchains.append(current_subchain)

    improved_chains: List[List[Link]] = list()
    for subchain in subchains:
        improved_links = sort_links(subchain)
        improved_links = combine_translations(improved_links)
        improved_chains.append(improved_links)

    improved_chain: List[Link] = list()
    for chain, keepsie in zip(improved_chains, keepsies):
        improved_chain += chain
        improved_chain += [keepsie]
    improved_chain += improved_chains[-1]

    return improved_chain
