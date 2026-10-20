// Exports the SF Symbols used on the Icons · System Comparison page as PNGs.
// Run on a Mac from the repo root:   swift scripts/export_sf_symbols.swift
// Output: assets/sf-symbols/<name>.png (one per symbol, 72 px, black on transparent)
//         assets/sf-symbols/pdf/<name>.pdf (vector, for SVG conversion)
//         assets/sf-symbols/_sheet.png + _sheet.json (all symbols on one grid, for Figma import)
// SF Symbols licence: use only in mockups of apps for Apple platforms.
import AppKit

let names = ["magnifyingglass", "gearshape", "square.and.arrow.up", "bookmark", "bookmark.fill", "house", "line.3.horizontal", "bell", "newspaper", "gamecontroller.fill", "chevron.up", "chevron.down", "chevron.left", "chevron.right", "xmark", "xmark.circle.fill", "person.circle.fill", "exclamationmark.triangle.fill", "envelope.fill", "arrow.clockwise", "line.3.horizontal.decrease", "textformat.size.smaller", "textformat.size.larger", "plus.circle", "minus.circle", "checkmark.circle.fill", "circle", "arrow.right.circle.fill", "arrow.up.left.and.arrow.down.right", "arrow.down.right.and.arrow.up.left", "arrow.left", "arrow.right", "play.fill", "pause.fill", "gobackward.15", "goforward.15", "backward.fill", "forward.fill", "cube", "star", "star.leadinghalf.filled", "star.fill", "heart", "arrow.2.squarepath", "checkmark.seal.fill", "apple.logo"]

let outDir = URL(fileURLWithPath: "assets/sf-symbols")
let pdfDir = outDir.appendingPathComponent("pdf")
try! FileManager.default.createDirectory(at: pdfDir, withIntermediateDirectories: true)

// Vector export: draw the (untinted, monochrome) symbol into a PDF context so its paths stay vector.
func writePDF(_ name: String) {
    guard let base = NSImage(systemSymbolName: name, accessibilityDescription: name),
          let img = base.withSymbolConfiguration(
              NSImage.SymbolConfiguration(pointSize: 40, weight: .regular).applying(.preferringMonochrome()))
    else { return }
    var box = CGRect(origin: .zero, size: img.size)
    let url = pdfDir.appendingPathComponent("\(name).pdf")
    guard let ctx = CGContext(url as CFURL, mediaBox: &box, nil) else { return }
    ctx.beginPDFPage(nil)
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(cgContext: ctx, flipped: false)
    img.draw(in: box)
    NSGraphicsContext.restoreGraphicsState()
    ctx.endPDFPage()
    ctx.closePDF()
}

let cell = 72          // px per symbol cell
let pointSize: CGFloat = 40
let cols = 8
let rows = (names.count + cols - 1) / cols

func bitmap(_ w: Int, _ h: Int) -> NSBitmapImageRep {
    NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: w, pixelsHigh: h, bitsPerSample: 8,
                     samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
                     colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
}
func symbol(_ name: String) -> NSImage? {
    guard let base = NSImage(systemSymbolName: name, accessibilityDescription: name) else { return nil }
    // Monochrome rendering keeps knock-outs (e.g. the x inside xmark.circle.fill) transparent.
    let cfg = NSImage.SymbolConfiguration(pointSize: pointSize, weight: .regular)
        .applying(.preferringMonochrome())
    guard let img = base.withSymbolConfiguration(cfg) else { return nil }
    // Tint to solid black, preserving the symbol's alpha.
    return NSImage(size: img.size, flipped: false) { r in
        img.draw(in: r)
        NSColor.black.set()
        r.fill(using: .sourceAtop)
        return true
    }
}
func draw(_ img: NSImage, centeredIn rect: NSRect) {
    let s = img.size
    img.draw(in: NSRect(x: rect.midX - s.width / 2, y: rect.midY - s.height / 2, width: s.width, height: s.height))
}

let sheet = bitmap(cols * cell, rows * cell)
sheet.size = NSSize(width: cols * cell, height: rows * cell)
var index: [[String: Any]] = []
var missing: [String] = []

for (i, name) in names.enumerated() {
    guard let img = symbol(name) else { missing.append(name); print("MISSING \(name)"); continue }
    // single PNG
    let rep = bitmap(cell, cell); rep.size = NSSize(width: cell, height: cell)
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
    draw(img, centeredIn: NSRect(x: 0, y: 0, width: cell, height: cell))
    NSGraphicsContext.restoreGraphicsState()
    try! rep.representation(using: .png, properties: [:])!.write(to: outDir.appendingPathComponent("\(name).png"))
    // sheet (AppKit origin is bottom-left; index uses top-left)
    let c = i % cols, r = i / cols
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: sheet)
    draw(img, centeredIn: NSRect(x: c * cell, y: (rows - 1 - r) * cell, width: cell, height: cell))
    NSGraphicsContext.restoreGraphicsState()
    writePDF(name)
    index.append(["name": name, "x": c * cell, "y": r * cell, "w": cell, "h": cell])
    print("ok \(name)")
}
try! sheet.representation(using: .png, properties: [:])!.write(to: outDir.appendingPathComponent("_sheet.png"))
let meta: [String: Any] = ["cell": cell, "cols": cols, "rows": rows, "width": cols * cell, "height": rows * cell,
                           "macOS": ProcessInfo.processInfo.operatingSystemVersionString, "symbols": index, "missing": missing]
try! JSONSerialization.data(withJSONObject: meta, options: [.prettyPrinted, .sortedKeys])
    .write(to: outDir.appendingPathComponent("_sheet.json"))
print("Done: \(index.count) exported, \(missing.count) missing → assets/sf-symbols/")
