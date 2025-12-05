import tkinter as tk
from tkinter import scrolledtext

# ================= S-BOX =================
aes_sbox = [
    [0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76],
    [0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0],
    [0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15],
    [0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75],
    [0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84],
    [0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf],
    [0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8],
    [0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2],
    [0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73],
    [0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb],
    [0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79],
    [0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08],
    [0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a],
    [0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e],
    [0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf],
    [0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16],
]

# ================ RCON ================
rcon = [0x00,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]

# ================ HELPERS ================
def sub_byte(b):
    return aes_sbox[b >> 4][b & 0x0F]

def rot_word(w):
    return w[1:] + w[:1]

def sub_word(w):
    return [sub_byte(x) for x in w]

def pretty_mat(m):
    return "\n".join(" ".join(f"{m[r][c]:02X}" for c in range(4)) for r in range(4))

def to_hex(b): return f"{b:02X}"
def to_bin8(b): return format(b, "08b")

def hex_with_subscript(hex_str):
    # return like "55₁₆" — but subscripts not supported everywhere; we'll append "(16)"
    return f"{hex_str}₁₆"

def bin_with_subscript(bin_str):
    return f"{bin_str}₂"

def show_hex_bin(byte):
    hx = to_hex(byte)
    bx = to_bin8(byte)
    return f"{hx}₁₆ = {bx}₂"

# GF(2^8) multiplication with explanation steps (bit-level)
def gmul_steps(a, b):
    """Return (result, explanation_lines) performing multiplication a * b in GF(2^8)."""
    lines = []
    lines.append(f"Multiply {to_hex(a)} by {to_hex(b)}:")
    a_val = a
    res = 0
    for i in range(8):
        if (b >> i) & 1:
            lines.append(f"  bit {i} of multiplier is 1 -> XOR with {to_hex(a_val)}")
            res ^= a_val
        else:
            lines.append(f"  bit {i} of multiplier is 0 -> skip")
        # show shift of a_val for next bit
        carry = (a_val & 0x80) != 0
        a_shift = (a_val << 1) & 0xFF
        if carry:
            a_shift ^= 0x1B
            lines.append(f"  shift: {to_hex(a_val)} << 1 -> {to_hex((a_val<<1)&0xFF)} then XOR 0x1B -> {to_hex(a_shift)} (carry)")
        else:
            lines.append(f"  shift: {to_hex(a_val)} << 1 -> {to_hex(a_shift)} (no carry)")
        a_val = a_shift
    lines.append(f"Result (hex): {to_hex(res)}")
    return res, lines

def gmul(a, b):
    # efficient standard gmul without steps
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        carry = a & 0x80
        a <<= 1
        a &= 0xFF
        if carry:
            a ^= 0x1B
        b >>= 1
    return p & 0xFF

def mix_single_column_steps(col):
    """Return (out_col, explanation_lines) for mix column with detailed steps."""
    a0,a1,a2,a3 = col
    lines = []
    lines.append(f"MixColumn on column: {' '.join(to_hex(x) for x in col)}")
    # compute 02*a0, 03*a1 etc with steps
    m02_a0, s02_a0 = gmul_steps(a0, 0x02)
    m02_a1, s02_a1 = gmul_steps(a1, 0x02)
    m02_a2, s02_a2 = gmul_steps(a2, 0x02)
    m02_a3, s02_a3 = gmul_steps(a3, 0x02)
    m03_a0 = m02_a0 ^ a0
    m03_a1 = m02_a1 ^ a1
    m03_a2 = m02_a2 ^ a2
    m03_a3 = m02_a3 ^ a3

    # R0 = 02*a0 ^ 03*a1 ^ a2 ^ a3
    r0 = m02_a0 ^ m03_a1 ^ a2 ^ a3
    r1 = a0 ^ m02_a1 ^ m03_a2 ^ a3
    r2 = a0 ^ a1 ^ m02_a2 ^ m03_a3
    r3 = m03_a0 ^ a1 ^ a2 ^ m02_a3

    # append steps
    lines.append("Detailed 02* and 03* steps for each byte:")
    lines.append(f" 02*{to_hex(a0)} -> {to_hex(m02_a0)}")
    lines += ["    "+ln for ln in s02_a0]
    lines.append(f" 03*{to_hex(a1)} -> {to_hex(m03_a1)} (03 = 02 XOR 01)")
    lines += ["    "+ln for ln in s02_a1]
    lines.append(f"    03*{to_hex(a1)} = 02*{to_hex(a1)} XOR {to_hex(a1)} -> {to_hex(m03_a1)}")
    lines.append(f" 02*{to_hex(a2)} -> {to_hex(m02_a2)}")
    lines += ["    "+ln for ln in s02_a2]
    lines.append(f" 03*{to_hex(a3)} -> {to_hex(m03_a3)}")
    lines += ["    "+ln for ln in s02_a3]
    lines.append("Combine with XOR for each result byte:")
    lines.append(f" R0 = 02*{to_hex(a0)} ⊕ 03*{to_hex(a1)} ⊕ {to_hex(a2)} ⊕ {to_hex(a3)} = {to_hex(r0)}")
    lines.append(f" R1 = {to_hex(a0)} ⊕ 02*{to_hex(a1)} ⊕ 03*{to_hex(a2)} ⊕ {to_hex(a3)} = {to_hex(r1)}")
    lines.append(f" R2 = {to_hex(a0)} ⊕ {to_hex(a1)} ⊕ 02*{to_hex(a2)} ⊕ 03*{to_hex(a3)} = {to_hex(r2)}")
    lines.append(f" R3 = 03*{to_hex(a0)} ⊕ {to_hex(a1)} ⊕ {to_hex(a2)} ⊕ 02*{to_hex(a3)} = {to_hex(r3)}")
    return [r0,r1,r2,r3], lines

# ================ KEY EXPANSION ================
def key_expansion_with_steps(key_hex):
    kb = [int(key_hex[i:i+2],16) for i in range(0,32,2)]
    key_mat = [[kb[r*4 + c] for c in range(4)] for r in range(4)]  # row-major
    w = []
    for c in range(4):
        w.append([key_mat[r][c] for r in range(4)])  # column as word
    steps = []
    steps.append(("init", [word.copy() for word in w[:4]]))
    for i in range(4,44):
        temp = w[i-1].copy()
        detail = {"i":i, "temp_before": temp.copy(), "rot":None, "sub":None, "rcon":None, "new":None}
        if i % 4 == 0:
            rw = rot_word(temp)
            sw = sub_word(rw)
            sw_after = sw.copy()
            sw_after[0] ^= rcon[i//4]
            detail["rot"] = rw
            detail["sub"] = sw
            detail["rcon"] = sw_after
            temp = sw_after
        neww = [w[i-4][j] ^ temp[j] for j in range(4)]
        detail["new"] = neww
        w.append(neww)
        steps.append(("gen", detail))
    return w, steps, key_mat

def round_key_matrix_from_w(w, r):
    start = r*4
    rk = [[0]*4 for _ in range(4)]
    for c in range(4):
        word = w[start+c]
        for row in range(4):
            rk[row][c] = word[row]
    return rk

# ================ AES STEP FUNCTIONS ================
def add_round_key(state, rk, explain=False):
    out = [[(state[r][c] ^ rk[r][c]) & 0xFF for c in range(4)] for r in range(4)]
    if explain:
        lines = []
        lines.append("AddRoundKey (per byte XOR):")
        for r in range(4):
            for c in range(4):
                a = state[r][c]
                b = rk[r][c]
                ax = to_bin8(a); bx = to_bin8(b)
                xor_res = a ^ b
                lines.append(f" {to_hex(a)} ({ax}₂) XOR {to_hex(b)} ({bx}₂) = {to_hex(xor_res)} ({to_bin8(xor_res)}₂)")
        return out, lines
    return out, []

def sub_bytes_with_steps(state):
    out = [[0]*4 for _ in range(4)]
    lines = ["SubBytes mapping (S-Box lookup):"]
    for r in range(4):
        for c in range(4):
            b = state[r][c]
            hx = to_hex(b)
            row = b >> 4
            col = b & 0x0F
            s = aes_sbox[row][col]
            out[r][c] = s
            lines.append(f" {hx} -> row {row}, col {col:X} -> SBOX[{row}][{col:X}] = {to_hex(s)}")
    return out, lines

def shift_rows_with_steps(state):
    out = [[0]*4 for _ in range(4)]
    lines = ["ShiftRows (row-major shifts):"]
    for r in range(4):
        row = state[r]
        shifted = row[r:] + row[:r]
        for c in range(4):
            out[r][c] = shifted[c]
        lines.append(f" Row {r} shift {r}: " + " ".join(to_hex(x) for x in row) + " -> " + " ".join(to_hex(x) for x in shifted))
    return out, lines

def mix_columns_with_steps(state):
    out = [[0]*4 for _ in range(4)]
    lines = ["MixColumns (detailed GF steps):"]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        mixed, mlines = mix_single_column_steps(col)
        for r in range(4):
            out[r][c] = mixed[r]
        lines.append(f" Column {c}: input {' '.join(to_hex(x) for x in col)} -> output {' '.join(to_hex(x) for x in mixed)}")
        lines += ["   "+ln for ln in mlines]
    return out, lines

# ================ MAIN PROCESS & GUI ================
def run_full_process():
    key = entry_key.get()
    plain = entry_plain.get()
    output.delete(1.0, tk.END)

    if len(key) != 16 or len(plain) != 16:
        output.insert(tk.END, "Error: Key dan Plaintext harus 16 karakter ASCII.\n")
        return

    # ASCII -> HEX -> BIN (LANGKAH 1)
    key_hex = "".join(f"{ord(c):02X}" for c in key)
    plain_hex = "".join(f"{ord(c):02X}" for c in plain)
    output.insert(tk.END, "=== LANGKAH 1: Konversi ASCII → HEX → BIN ===\n")
    output.insert(tk.END, f"Plaintext ASCII: {plain}\n")
    output.insert(tk.END, f"Plaintext HEX : {plain_hex}\n")
    # show binary per byte with subscript style
    pbytes = [int(plain_hex[i:i+2],16) for i in range(0,32,2)]
    for i, b in enumerate(pbytes):
        output.insert(tk.END, f" P[{i}] = {to_hex(b)}₁₆ = {to_bin8(b)}₂\n")
    output.insert(tk.END, "\n")
    output.insert(tk.END, f"Cipher Key ASCII : {key}\n")
    output.insert(tk.END, f"Cipher Key HEX   : {key_hex}\n")
    kbytes = [int(key_hex[i:i+2],16) for i in range(0,32,2)]
    for i, b in enumerate(kbytes):
        output.insert(tk.END, f" K[{i}] = {to_hex(b)}₁₆ = {to_bin8(b)}₂\n")
    output.insert(tk.END, "\n")

    # LANGKAH 2: XOR plaintext dan cipher key per byte (show bitwise)
    output.insert(tk.END, "=== LANGKAH 2: XOR Plaintext ⊕ CipherKey (per byte, biner) ===\n")
    xor_res = []
    output.insert(tk.END, "Index | Plain HEX (bin)       | Key HEX (bin)         | XOR -> HEX (bin)\n")
    output.insert(tk.END, "---------------------------------------------------------------\n")
    for i in range(16):
        a = pbytes[i]; b = kbytes[i]
        xr = a ^ b
        output.insert(tk.END, f"{i:2d}    | {to_hex(a)} ({to_bin8(a)}₂) | {to_hex(b)} ({to_bin8(b)}₂) | {to_hex(xr)} ({to_bin8(xr)}₂)\n")
        xor_res.append(xr)
    output.insert(tk.END, "\n")

    # LANGKAH 3: Key Expansion with steps (RotWord/SubWord/Rcon)
    output.insert(tk.END, "=== LANGKAH 3: PEMBANGKITAN KUNCI (Key Expansion) ===\n")
    w, steps, key_mat = key_expansion_with_steps(key_hex)
    output.insert(tk.END, "Initial Key matrix (row-major):\n")
    output.insert(tk.END, pretty_mat(key_mat) + "\n\n")
    output.insert(tk.END, "K0..K10 (round keys) [displayed as row-major matrices built from column-words]:\n")
    for r in range(11):
        rk = round_key_matrix_from_w(w, r)
        output.insert(tk.END, f"K{r}:\n{pretty_mat(rk)}\n\n")
    # show steps for Rot/Sub/Rcon in detail
    output.insert(tk.END, "Detail Key Expansion (RotWord / SubWord / Rcon / NewWord):\n")
    for s in steps:
        if s[0] == "init":
            output.insert(tk.END, "Initial words (columns W0..W3):\n")
            init = s[1]
            for idx, ww in enumerate(init):
                output.insert(tk.END, f" W{idx}: " + " ".join(to_hex(b) for b in ww) + "\n")
            output.insert(tk.END, "\n")
        else:
            d = s[1]
            i = d["i"]
            output.insert(tk.END, f"i={i} temp_before: " + " ".join(to_hex(b) for b in d["temp_before"]) + "\n")
            if d["rot"] is not None:
                output.insert(tk.END, "  RotWord: " + " ".join(to_hex(b) for b in d["rot"]) + "\n")
                # show subword with S-Box coords
                output.insert(tk.END, "  SubWord (S-Box lookups):\n")
                for j, sb in enumerate(d["sub"]):
                    b = d["rot"][j]
                    row = b >> 4
                    col = b & 0x0F
                    sboxv = d["sub"][j]
                    output.insert(tk.END, f"    byte {j}: {to_hex(b)} -> row {row}, col {col:X} -> {to_hex(sboxv)}\n")
                output.insert(tk.END, "  After Rcon XOR (on first byte): " + " ".join(to_hex(b) for b in d["rcon"]) + "\n")
            output.insert(tk.END, "  New word (w{}): ".format(i) + " ".join(to_hex(b) for b in d["new"]) + "\n\n")

    # Build initial state (row-major per your PDF)
    state = [[pbytes[r*4 + c] for c in range(4)] for r in range(4)]
    output.insert(tk.END, "=== INITIAL STATE (row-major as in PDF) ===\n")
    output.insert(tk.END, pretty_mat(state) + "\n\n")

    # INITIAL AddRoundKey (Round 0) — show per-bit XOR details
    output.insert(tk.END, "=== ROUND 0: Initial AddRoundKey ===\n")
    rk0 = round_key_matrix_from_w(w, 0)
    output.insert(tk.END, "Round Key K0:\n" + pretty_mat(rk0) + "\n\n")
    out0, lines = add_round_key(state, rk0, explain=True)
    for ln in lines:
        output.insert(tk.END, ln + "\n")
    state = out0
    output.insert(tk.END, "\nState after AddRoundKey:\n" + pretty_mat(state) + "\n\n")

    # Rounds 1..9: SubBytes -> ShiftRows -> MixColumns -> AddRoundKey (detailed)
    for r in range(1, 10):
        output.insert(tk.END, f"========== ROUND {r} ==========\n")
        # SubBytes
        sb_state, sb_lines = sub_bytes_with_steps(state)
        output.insert(tk.END, "🔹 SubBytes:\n")
        for ln in sb_lines:
            output.insert(tk.END, ln + "\n")
        output.insert(tk.END, "State after SubBytes:\n" + pretty_mat(sb_state) + "\n\n")

        # ShiftRows
        sr_state, sr_lines = shift_rows_with_steps(sb_state)
        output.insert(tk.END, "🔹 ShiftRows:\n")
        for ln in sr_lines:
            output.insert(tk.END, ln + "\n")
        output.insert(tk.END, "State after ShiftRows:\n" + pretty_mat(sr_state) + "\n\n")

        # MixColumns
        mc_state, mc_lines = mix_columns_with_steps(sr_state)
        output.insert(tk.END, "🔹 MixColumns:\n")
        for ln in mc_lines:
            output.insert(tk.END, ln + "\n")
        output.insert(tk.END, "State after MixColumns:\n" + pretty_mat(mc_state) + "\n\n")

        # AddRoundKey
        rk = round_key_matrix_from_w(w, r)
        output.insert(tk.END, "Round Key K" + str(r) + ":\n" + pretty_mat(rk) + "\n\n")
        state, add_lines = add_round_key(mc_state, rk, explain=True)
        output.insert(tk.END, "After AddRoundKey (per-byte):\n")
        for ln in add_lines:
            output.insert(tk.END, ln + "\n")
        output.insert(tk.END, "\nState after AddRoundKey:\n" + pretty_mat(state) + "\n\n")

    # Round 10 (no MixColumns)
    output.insert(tk.END, "========== ROUND 10 ==========\n")
    sb_state, sb_lines = sub_bytes_with_steps(state)
    output.insert(tk.END, "🔹 SubBytes:\n")
    for ln in sb_lines:
        output.insert(tk.END, ln + "\n")
    output.insert(tk.END, "State after SubBytes:\n" + pretty_mat(sb_state) + "\n\n")

    sr_state, sr_lines = shift_rows_with_steps(sb_state)
    output.insert(tk.END, "🔹 ShiftRows:\n")
    for ln in sr_lines:
        output.insert(tk.END, ln + "\n")
    output.insert(tk.END, "State after ShiftRows:\n" + pretty_mat(sr_state) + "\n\n")

    rk10 = round_key_matrix_from_w(w, 10)
    output.insert(tk.END, "Round Key K10:\n" + pretty_mat(rk10) + "\n\n")
    state, add_lines = add_round_key(sr_state, rk10, explain=True)
    output.insert(tk.END, "After AddRoundKey (Final, per-byte):\n")
    for ln in add_lines:
        output.insert(tk.END, ln + "\n")
    output.insert(tk.END, "\nFinal Ciphertext state:\n" + pretty_mat(state) + "\n\n")

    # Final ciphertext as row-major HEX
    chex = "".join(to_hex(state[r][c]) for r in range(4) for c in range(4))
    output.insert(tk.END, f"=== CIPHERTEXT (HEX, row-major): {chex} ===\n")

# ======== Build Tkinter UI ========
root = tk.Tk()
root.title("AES Pendidikan — SUPER DETAIL (seperti PDF) — Tkinter")
root.geometry("1000x720")

frm = tk.Frame(root)
frm.pack(pady=6)

tk.Label(frm, text="Cipher Key (16 ASCII chars):").grid(row=0, column=0, sticky="w")
entry_key = tk.Entry(frm, width=40)
entry_key.grid(row=0, column=1, padx=8)

tk.Label(frm, text="Plaintext (16 ASCII chars):").grid(row=1, column=0, sticky="w")
entry_plain = tk.Entry(frm, width=40)
entry_plain.grid(row=1, column=1, padx=8)

btn_run = tk.Button(root, text="Run (SUPER DETAIL like PDF)", command=run_full_process)
btn_run.pack(pady=8)

output = scrolledtext.ScrolledText(root, width=130, height=38)
output.pack(padx=8, pady=6)

root.mainloop()
