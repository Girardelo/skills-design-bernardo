# Skills de design de sistemas e interface (Bernardo)

Quatro skills para o Claude Code (ou qualquer IA que leia `SKILL.md`):

| Skill | Para que serve |
| --- | --- |
| `design-de-sistemas` | Planejar, criar e melhorar telas de sistemas, apps e painéis, uma parte por vez, com opções e régua de qualidade |
| `branding-identity-standard` | Marca, identidade visual, nome e logo com resultado premium |
| `diretor-visual-global` | Artes, criativos, banners, posts e carrosséis |
| `website-design-moa` | Time de vários agentes para desenhar site (só quando pedido pelo nome) |

A pasta `contexto/` tem as notas de apoio que as skills citam: referências de interface aprovadas, o jeito de criar telas e o padrão de tela e página.

## Como instalar (pedir para a IA)

Cole isto na tua IA:

> Clona o repositório `https://github.com/Girardelo/skills-design-bernardo` e copia cada pasta de `skills/` para `~/.claude/skills/`. Copia também a pasta `contexto/` para `~/.claude/skills/contexto/`. Depois me lista as skills instaladas.

Ou no terminal:

```bash
git clone https://github.com/Girardelo/skills-design-bernardo.git
cp -R skills-design-bernardo/skills/* ~/.claude/skills/
cp -R skills-design-bernardo/contexto ~/.claude/skills/contexto
```

Observação: alguns trechos citam caminhos do Mac do Bernardo (Brain, Codex). São referências dele; a skill funciona sem eles.
