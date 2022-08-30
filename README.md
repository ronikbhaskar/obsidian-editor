# Obsidian as an Editor

This file was created using `obsidian.py`.

## Background

I have no issues with what Obsidian is. My only complaint is with what it *isn't*: a Markdown editor.

I know you can edit Markdown in Obsidian, but that's not what I'm talking about. I mean editing *any* .md file in Obsidian. Right now, you're limited to your vault, which makes sense, since Obsidian is a note-taking app--a second brain app. Everything you need is right there in your vault. The thing is, I don't really care for the whole "second brain" thing. I tried it for a bit, but it really didn't stick. It's a nice place to put notes if I don't know where else to put them, but sometimes I just wanna edit a Markdown file with Obsidian's QoL. 

## The Hack

I don't call this a hack to be arrogant or even facetious. I just mean I wanted to make technology do something it wasn't created to do. I wanted to turn Obsidian into an editor. 

There are a few approaches to this method. The first that probably comes to most people's minds is to edit Obsidian's view of your file system so it thinks your whole computer is a vault. I didn't do that, but that would be really cool. Instead, I just wrote a script that copies your .md file into your vault and copies it back when you're done. Definitely not the most elegant solution, but it works for my purposes.

## Setbacks

The issues with this project were unrelated to the actual manipulation of the vault. Instead, I realized that in order to take advantage of Obsidian's features, I would have to engineer changes on top of them to make them compatible with any mainstream Markdown editor. 

In particular, Obsidian's image linking is fantastic, especially combined with their drag-and-drop feature for images. The problem is that Markdown doesn't usually support images linked like this: ![[image.img]]

So, I had to find all the instances of images like those, reformat them, and when copying the Markdown, copy the linked files as well. While I did learn a bit more about regex in the process, the solution is quite messy and works under fairly strong assumptions. Nevertheless, it works.

## Improvements

Image-linking isn't the only useful feature in Obsidian. Making more of these QoL standards available through this script means I can take full advantage of the tools Obsidian offers. For example, linking pdfs, better tables, and tags would all be fantastic if I could integrate / hide them seamlessly with this script. Or, I could add `scp` support so I can use this on ssh servers. 

I probably won't do any of that that, since I don't really like doing more than making quick prototypes to prove that I can. Who knows? Maybe some day.

For now, I'll see you in the next project.
