docker::image {'stianstrom/purserworker':
image_tag => 'latest'
 }

docker::run { 'webuseworker1':
  image   => 'stianstrom/webuseworker',
}
docker::run { 'webuseworker2':
  image   => 'stianstrom/webuseworker',
}
docker::run { 'purserworker1':
  image   => 'stianstrom/purserworker',
}
docker::run { 'purserworker2':
  image   => 'stianstrom/purserworker',
}
docker::run { 'httperfworker1':
  image   => 'stianstrom/httperworker',
}
docker::run { 'httperfworker2':
  image   => 'stianstrom/httperworker',
}
}
