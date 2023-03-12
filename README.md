# inventree-zpl-plugin

ZPL (Zebra Printer Language) plugin for [InvenTree](https://inventree.org/). This plugin uses a [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) ZPL template to generate barcode labels for parts and stock items, then sends the generated ZPL directly to a network-attached ZPL-capable printer (such as the Zebra GK420t).

![](https://ss.ycnrg.org/jotunn_20230312_013013.png)

## Config Options

* `HOSTNAME` - Hostname or IP address of the target printer
* `PORT` - Port number (default: `9100`; should be used in most cases)
* `TIMEOUT` - Socket timeout in seconds (default: `15`)
* `TEMPLATE_PATH` - Absolute filesystem path to the Jinja2 template

When running inside of Docker, place the template file in your "data" mount directory. The path would then become `/home/inventree/data/example_2x1.j2`.

# Customizing the Template

The template file can be edited or changed without needing to restart Inventree or the Docker services. This can allow you to make changes or tweaks quickly.

For overall design, it is recommended to use the [Labelary Online Viewer](http://labelary.com/viewer.html). Make sure to set the correct label size, then you can make edits to the ZPL source and preview the result. This is best done with test data, since obviously the Labelary viewer is not going to be able to interpret the Jinja2 template. Once you're satisfied with the design, re-add the template variables and control blocks. Final testing on your actual printer will still be necessary, as the printer is the one actually rendering the barcodes, fonts, and graphics -- capabilities can vary slightly between printer models and firmware versions.

For a more in-depth look at using ZPL, check out Labelary's [Introduction to ZPL](http://labelary.com/zpl.html) page.

> [ZPL Command Reference](http://labelary.com/docs.html)

> [Jinja Template Designer Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)

## Template Fields

The following fields are available inside of the template:

* `name` - Part name (ex. `CR0603-FX-1402ELF`)
* `description` - Part description (ex. `Thick Film 14K 1% 1/10W`)
* `ipn` - Part IPN (ex. `123123-44412`)
* `pk` - Part ID/Primary Key (ex. `405`)
* `params` - Parameter map/dict (ex. `{Package: "SMD 0603", "Resistance": "14k"}`)
* `category` - Category name (ex. `Resistor`)
* `category_path` - Category path (ex. `Passive/Resistor`)
* `part` - The full `Part` object from InvenTree. This can be used for accessing other values not provided above.

# Why use ZPL?

So why use ZPL for printing labels instead of rendering them to PDF or PNG first and then rasterizing them?

1. Printing directly to the printer is very fast (no need for printer drivers, CUPS, etc.). From the time you choose to print the label until the time it's finished printing is usually around 1 second. This also means bulk-printing dozens or hundreds of labels is equally fast. When using an OS print driver with a label printer, this can be considerably slower.
2. In a multi-user environment, users of the system don't have to worry about installing print drivers or permissions just to print part labels to a shared printer. The printing is handled by the InvenTree worker.
3. Since ZPL is purpose-built for labels, templates can be easier to write than CSS and HTML. You also let the printer handle generating the barcodes.
4. Good print quality -- no need to worry about antialiasing, scaling, or dithering artifacts. This is especially important for small barcodes and text when most thermal printers only have 203 or 300 dpi.

## What are the downsides?

1. You need to create a different template for each label size you wish to print
2. The InvenTree worker must have network access to the printer. This could be a problem if you run InvenTree from a remote VPS or cloud environment (this could be overcome with a tunnel or VPN, but may not be worth it).
3. Custom graphics and fonts can be a pain to work with. It is possible to upload custom images and fonts to most printers, then recall them later (see FAQ). ZPL also supports in-line bitmap graphics, but this will make your templates huge and cumbersome to manage.

![](https://ss.ycnrg.org/jotunn_20230312_013159.png)

# FAQ

## How to use a custom font?
To use a custom font (other than the ones that come pre-installed on the printer as standard ZPL fonts), you must transfer it to the printer first. Once stored, they can be recalled using the `^A@` ZPL command.  This varies by printer, check the [Zebra documentation](https://supportcommunity.zebra.com/s/article/Downloading-and-Using-Fonts-on-Zebra-ZPL-Printers) for details.

## How to use a custom logo or image on every label?
Most printers support downloading images to their local flash memory. These images are stored in a special `GRF` format. The images can then be recalled later by using the `^XG` ZPL command. Check the [Zebra documentation](https://supportcommunity.zebra.com/s/article/Convert-Download-and-Print-Graphics-to-a-ZPL-compatible-Zebra-Printer) for details.


