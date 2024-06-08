module.exports = {
  title: "Nan Quest",
  summary: "MSPFA",
  
  edit: true,

  trees: {
    './': 'assets://mspfa/Nan Quest/',
  },
  async asyncComputed(api) {
    const story = await api.readYamlAsync("./story.yaml")
    return {
      styles: [
        {body: await api.readFileAsync("./adventure.scss")}
      ],
      edit(archive){
        archive.mspfa['Nan Quest'] = story
      }
    }
  }
}
