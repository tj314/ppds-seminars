
# Table of Contents

1.  [Inštalácia](#org406c55f)
2.  [Používanie](#orged47b4e)
3.  [Integrácia s editormi](#org42f7ec4)
    1.  [VS Code](#org785e526)
    2.  [PyCharm](#org001330b)
    3.  [Iný](#org9975fa1)

V zadaniach vyžadujeme, aby ste dodržiavali štandardy PEP 8 a PEP 257 pre
písanie kódu a dokumentačných reťazcov. Aby ste nemuseli tieto pravidlá
kontrolovať manuálne, pripravili sme konfiguráciu pre nástroj `ruff`, ktorý
kontrolu automatizuje a vie väčšinu chýb opraviť.


<a id="org406c55f"></a>

# Inštalácia

Ak ešte **nemáte** vytvorené virtuálne prostredie pre svoj repozitár, vytvorte ho.
V koreňovom priečinku repozitára vykonajte (pre Windows použite `py` alebo
`python` namiesto `python3`):

    python3 -m venv .venv

Virtuálne prostredie potom aktivujte. Na Linuxe:

    source .venv/bin/activate

Na Windowse v PowerShelli:

    .venv\Scripts\Activate.ps1

Ak to na Windowse nefunguje, v PowerShelli vykonajte

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

a skúste znova.

Na začiatku *promptu* terminálu by ste teraz mali vidieť `(.venv)`. Ak tam nie
je, virtuálne prostredie nebolo aktivované!

Nainštalujte `ruff` (prípadne aj `fei.ppds`):

    pip install ruff

Do koreňového priečinka repozitára potom uložte [pyproject.toml](pyproject.toml) (alebo ho
vytvorte a skopírujte obsah).


<a id="orged47b4e"></a>

# Používanie

Príkaz

    ruff check [FILES]...

vypíše nájdené problémy v súboroch `FILES`. Ak neuvediete cesty k súborom,
skontroluje všetky súbory v priečinku.

Príkaz

    ruff check --fix [FILES]...

automaticky opraví problémy v súboroch a vypíše tie, ktoré musíte manuálne
opraviť.

Voliteľne môžete spustiť aj formátovanie, ktoré vykoná úpravy naviac oproti
PEP 8:

    ruff format [FILES]...

Pre viac informácií sa poraďte s [dokumentáciou projektu](https://docs.astral.sh/ruff/linter/). Ak by ste našli nejaké
problémy v konfigurácii, mali nápady alebo pripomienky, ozvite sa.


<a id="org42f7ec4"></a>

# Integrácia s editormi

`ruff` je možné aktivovať priamo z vášho obľúbeného editora.


<a id="org785e526"></a>

## VS Code

Nainštalujte doplnok z [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff).


<a id="org001330b"></a>

## PyCharm

Nainštalujte neoficiálny doplnok z [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/20574-ruff).


<a id="org9975fa1"></a>

## Iný

Používate iný editor? Napíšte mi a pridám sem návod. Zvyšné návody sú
k dispozícii v [dokumentácii pre ruff](https://docs.astral.sh/ruff/editors/setup/).

